import cv2
import argparse
from ultralytics import YOLO
import numpy as np
import datetime

# Define a restricted zone as a polygon (roughly bottom-right quarter of a 1280x720 frame)
RESTRICTED_ZONE_POLYGON = np.array([[640, 360], [1280, 360], [1280, 720], [640, 720]], np.int32)

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

    zone_status = {} # Track ID -> bool (is_inside)
    frame_count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            print("End of video stream or error reading frame.")
            break

        frame_count += 1
        if frame_count % 30 == 0:
            print(f"[DEBUG] Frame shape: {frame.shape}")

        # Run YOLO tracking
        results = model.track(frame, persist=True, verbose=False)

        # Draw the restricted zone
        print(f"[DEBUG] Drawing zone at coordinates: {RESTRICTED_ZONE_POLYGON.tolist()}")
        cv2.polylines(frame, [RESTRICTED_ZONE_POLYGON], isClosed=True, color=(0, 0, 255), thickness=2)
        cv2.putText(frame, "RESTRICTED ZONE", (RESTRICTED_ZONE_POLYGON[0][0], RESTRICTED_ZONE_POLYGON[0][1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

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

                # Track ID
                track_id = int(box.id[0]) if box.id is not None else None

                # Default bounding box color
                color = (0, 255, 0)
                thickness = 2

                # Restricted zone logic
                if cls_name == "person" and track_id is not None:
                    # Calculate reference point (bottom-center)
                    x_center = (x1 + x2) // 2
                    y_bottom = y2
                    
                    # Check if inside polygon
                    test_result = cv2.pointPolygonTest(RESTRICTED_ZONE_POLYGON, (x_center, y_bottom), False)
                    print(f"[DEBUG] Track ID: {track_id} | Ref Point: ({x_center}, {y_bottom}) | pointPolygonTest: {test_result}")
                    is_inside = test_result >= 0
                    was_inside = zone_status.get(track_id, False)
                    
                    if is_inside and not was_inside:
                        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        print(f"[EVENT] Restricted Zone Crossing - Track ID: {track_id} - Time: {timestamp}")
                        
                    zone_status[track_id] = is_inside
                    
                    if is_inside:
                        color = (0, 0, 255) # Red for inside

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
