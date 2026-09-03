import cv2
import argparse
from ultralytics import YOLO

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

    while True:
        ret, frame = cap.read()
        if not ret:
            print("End of video stream or error reading frame.")
            break

        # Run YOLO detection
        results = model(frame, verbose=False)

        for result in results:
            boxes = result.boxes
            for box in boxes:
                # Bounding box coordinates
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                
                # Confidence score
                conf = float(box.conf[0])
                
                # Class name
                cls_id = int(box.cls[0])
                cls_name = model.names[cls_id]

                # Print to terminal
                print(f"Detected: {cls_name} | Confidence: {conf:.2f} | BBox: ({x1}, {y1}, {x2}, {y2})")

                # Draw bounding box and label
                color = (0, 255, 0)
                thickness = 2
                cv2.rectangle(frame, (x1, y1), (x2, y2), color, thickness)
                
                label = f"{cls_name} {conf:.2f}"
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
