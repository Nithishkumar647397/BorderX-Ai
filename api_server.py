import asyncio
import json
import threading
import datetime
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import uvicorn

# Import the refactored detection logic
from detect_test import run_detection

app = FastAPI(title="BORDER-X API Backend")

# Maintain a list of active websocket connections
class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        # Convert dict to JSON string
        message_str = json.dumps(message)
        # Create a copy to avoid issues if connections drop during iteration
        for connection in list(self.active_connections):
            try:
                await connection.send_text(message_str)
            except WebSocketDisconnect:
                self.disconnect(connection)
            except Exception as e:
                print(f"Error sending message to client: {e}")
                self.disconnect(connection)

manager = ConnectionManager()

# We need an asyncio Queue to pass messages from the OpenCV background thread
# to the asyncio event loop.
event_queue = None
loop = None

# Global state to keep track of the latest people count for the heartbeat
current_tracked_people = 0

def opencv_event_callback(event_dict):
    """
    This callback is called from the OpenCV background thread.
    We need to safely push the event_dict to the main thread's asyncio queue.
    """
    global current_tracked_people
    if event_dict.get("type") == "frame_detections":
        current_tracked_people = event_dict.get("tracked_people_count", 0)

    if loop and event_queue:
        asyncio.run_coroutine_threadsafe(event_queue.put(event_dict), loop)

def start_opencv_thread():
    """
    Runs the YOLO detection loop in a separate thread so it doesn't block the FastAPI event loop.
    """
    print("Starting background OpenCV thread...")
    # Run on camera 0 by default, passing our callback
    run_detection(video_source="0", event_callback=opencv_event_callback)

@app.on_event("startup")
async def startup_event():
    global event_queue, loop
    loop = asyncio.get_running_loop()
    event_queue = asyncio.Queue()
    
    # Start the OpenCV blocking loop in a background daemon thread
    detection_thread = threading.Thread(target=start_opencv_thread, daemon=True)
    detection_thread.start()
    
    # Start the background task that consumes events and broadcasts them
    asyncio.create_task(event_broadcaster())
    
    # Start the heartbeat task
    asyncio.create_task(heartbeat_task())

async def event_broadcaster():
    """
    Consumes events from the queue and broadcasts to all WebSocket clients.
    """
    while True:
        try:
            event_dict = await event_queue.get()
            await manager.broadcast(event_dict)
            event_queue.task_done()
        except asyncio.CancelledError:
            break
        except Exception as e:
            print(f"Broadcaster error: {e}")
            await asyncio.sleep(1)

async def heartbeat_task():
    """
    Periodically sends a lightweight heartbeat message to clients.
    """
    global current_tracked_people
    while True:
        try:
            await asyncio.sleep(1)
            heartbeat_msg = {
                "type": "heartbeat",
                "timestamp": datetime.datetime.now().isoformat(),
                "people_count": current_tracked_people,
                "camera_status": "online" # Assuming online since the thread is running
            }
            await manager.broadcast(heartbeat_msg)
        except asyncio.CancelledError:
            break
        except Exception as e:
            print(f"Heartbeat error: {e}")
            await asyncio.sleep(1)

@app.websocket("/ws/events")
async def websocket_endpoint(websocket: WebSocket):
    """
    WebSocket endpoint for the dashboard to receive real-time events.
    """
    await manager.connect(websocket)
    try:
        # Keep the connection alive
        while True:
            # We don't expect messages from the client in this one-way broadcast setup,
            # but we need to wait/read to detect disconnects.
            data = await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception as e:
        print(f"WebSocket error: {e}")
        manager.disconnect(websocket)

if __name__ == "__main__":
    # To run this script: python api_server.py
    print("Starting BORDER-X API Server...")
    print("================================================================")
    print("WebSocket Server will run on: ws://localhost:8000/ws/events")
    print("================================================================")
    uvicorn.run("api_server:app", host="0.0.0.0", port=8000, log_level="info")

"""
-------------------------------------------------------------------------------
TESTING INSTRUCTIONS (Save this as a script to test or run in python terminal)
-------------------------------------------------------------------------------

import asyncio
import websockets
import json

async def test_ws():
    uri = "ws://localhost:8000/ws/events"
    print(f"Connecting to {uri}...")
    try:
        async with websockets.connect(uri) as websocket:
            print("Connected! Listening for events...\n")
            while True:
                message = await websocket.recv()
                data = json.loads(message)
                
                # Filter out heartbeat for a cleaner output, or comment out to see everything
                if data.get("type") != "heartbeat":
                    print(f"[EVENT] {json.dumps(data, indent=2)}\n")
    except Exception as e:
        print(f"Connection failed: {e}")

if __name__ == "__main__":
    asyncio.run(test_ws())
-------------------------------------------------------------------------------
"""
