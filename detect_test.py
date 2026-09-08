import cv2
import argparse
from ultralytics import YOLO
import numpy as np
import datetime
import time

LOITER_THRESHOLD_SECONDS = 90

def main():
    parser = argparse.ArgumentParser(description="BORDER-X YOLOv8 Object Detection Test")
    parser.add_argument("video_source", nargs="?", default="0", help="Path to video file or webcam index (default: 0)")
    args = parser.parse_args()

    # Determine if video_source is a file path or a camera index
    source = args.video_source
    if source.isdigit():
        source = int(source)

    # Load the YOLOv8 nano model
    print("Loading YOLOv8 model...")
    model = YOLO("yolov8n.pt")

    # Initialize video capture
    print(f"Opening video source: {source}")
    cap = cv2.VideoCapture(source)
    if not cap.isOpened():
        print(f"Error: Could not open video source {source}")
        return

    window_name = "BORDER-X - Detection Test"
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)

    print("Starting detection... Press 'q' to exit.")

    zone_status = {} # Track ID -> {'is_inside': bool, 'outside_frames': int}
    track_frames = {} # Track ID -> frames seen
    frame_count = 0
    restricted_zone_polygon = None

    while True:
        ret, frame = cap.read()
        if not ret:
            print("End of video stream or error reading frame.")
            break

        frame_count += 1

        if restricted_zone_polygon is None:
            height, width = frame.shape[:2]
            x_mid, y_mid = width // 2, height // 2
            restricted_zone_polygon = np.array([
                [x_mid, y_mid],
                [width, y_mid],
                [width, height],
                [x_mid, height]
            ], np.int32)

        # Run YOLO tracking
        # track_buffer controls how many consecutive frames the tracker keeps a lost track alive in memory before deleting it.
        # This helps maintain the same ID during temporary occlusions.
        results = model.track(frame, persist=True, conf=0.6, tracker="custom_tracker.yaml", verbose=False)

        # Draw the restricted zone
        cv2.polylines(frame, [restricted_zone_polygon], isClosed=True, color=(0, 0, 255), thickness=2)
        cv2.putText(frame, "RESTRICTED ZONE", (restricted_zone_polygon[0][0], restricted_zone_polygon[0][1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

        current_frame_tracks = set()
        for result in results:
            boxes = result.boxes
            if boxes is None:
                continue

            for box in boxes:
                # Bounding box coordinates
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                
                # Confidence score
                conf = float(box.conf[0])
                
                # Class name
                cls_id = int(box.cls[0])
                cls_name = model.names[cls_id]

                if cls_name != "person":
                    continue

                # Track ID
                track_id = int(box.id[0]) if box.id is not None else None
                if track_id is not None:
                    current_frame_tracks.add(track_id)

                # Default bounding box color
                color = (0, 255, 0)
                thickness = 2

                # Restricted zone logic
                if cls_name == "person" and track_id is not None:
                    # Update track frame counter
                    if track_id not in track_frames:
                        track_frames[track_id] = 0
                    track_frames[track_id] += 1

                    # Calculate reference point (bottom-center)
                    x_center = (x1 + x2) // 2
                    y_bottom = y2
                    
                    # Check if inside polygon
                    test_result = cv2.pointPolygonTest(restricted_zone_polygon, (x_center, y_bottom), False)
                    is_inside = test_result >= 0
                    
                    if track_id not in zone_status:
                        zone_status[track_id] = {'is_inside': False, 'outside_frames': 5, 'entry_time': None, 'loiter_event_fired': False}
                        
                    status = zone_status[track_id]
                    
                    if is_inside:
                        color = (0, 0, 255) # Red for inside
                        if track_frames[track_id] >= 10:
                            if not status['is_inside'] and status['outside_frames'] >= 5:
                                timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                                print(f"[EVENT] Restricted Zone Crossing - Track ID: {track_id} - Time: {timestamp}")
                                status['entry_time'] = time.time()
                                status['loiter_event_fired'] = False
                                
                            status['is_inside'] = True
                            status['outside_frames'] = 0
                            
                            if status['entry_time'] is not None:
                                elapsed = time.time() - status['entry_time']
                                if elapsed >= LOITER_THRESHOLD_SECONDS and not status['loiter_event_fired']:
                                    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                                    print(f"[EVENT] LOITERING DETECTED - Track ID: {track_id} - Duration: {elapsed:.1f}s - Time: {timestamp}")
                                    status['loiter_event_fired'] = True
                                
                                cv2.putText(frame, f"In Zone: {int(elapsed)}s", (x1, y2 + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
                    else:
                        status['is_inside'] = False
                        status['outside_frames'] += 1
                        if status['outside_frames'] >= 5:
                            status['entry_time'] = None
                            status['loiter_event_fired'] = False

                # Print to terminal
                if track_id is not None:
                    print(f"Detected: {cls_name} | ID: {track_id} | Confidence: {conf:.2f} | BBox: ({x1}, {y1}, {x2}, {y2})")
                    label = f"ID:{track_id} {cls_name} {conf:.2f}"
                else:
                    print(f"Detected: {cls_name} | Confidence: {conf:.2f} | BBox: ({x1}, {y1}, {x2}, {y2})")
                    label = f"{cls_name} {conf:.2f}"

                # Draw bounding box and label
                cv2.rectangle(frame, (x1, y1), (x2, y2), color, thickness)
                
                cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, thickness)

        for tid, status in zone_status.items():
            if tid not in current_frame_tracks:
                status['is_inside'] = False
                status['outside_frames'] += 1
                if status['outside_frames'] >= 5:
                    status['entry_time'] = None
                    status['loiter_event_fired'] = False

        # Display the frame
        cv2.imshow(window_name, frame)

        # Exit cleanly on 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release resources
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
