import cv2
from ultralytics import YOLO
import threading

# Load the YOLOv8 model
try: 
    model = YOLO('best.pt')
except Exception as e:
    print("Error loading YOLOv8 model:", e)
    exit()

# Open the video file
video_path = r"D:\Prathamesh_Data\object_count_camera_Baumer\10_brass_ring.mp4"
cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    print("Error opening video file")
    exit()

# Initialize object count and unique ID counter
object_count = 0
unique_id_counter = 1

# Confidence threshold
confidence_threshold = 0.5

# NMS (Non-Maximum Suppression) threshold
nms_threshold = 0.5

while cap.isOpened():
    # Read a frame from the video
    success, frame = cap.read()

    if success:
        # Run YOLOv8 tracking on the frame, persisting tracks between frames
        try:
            results = model.track(frame, iou=0.5, persist=True)
            annotated_frame = results[0].plot()  # Visualize the results on the frame

            # Get the count of detected objects in the current frame
            frame_object_count = len(results[0])

            # Loop through detected objects and display the count on the frame
            for i, obj in enumerate(results[0]):
                obj_id_attr = 'cnt'  
                obj_id_value = getattr(obj.boxes.id, obj_id_attr, None)

                tensor_value_attr = 'T' 
                tensor_value = getattr(obj.boxes.id, tensor_value_attr, None)

                if tensor_value is not None and isinstance(tensor_value, list) and len(tensor_value) > 0:
                    # If 'T' value is available and not empty, use it
                    value = float(tensor_value[0])
                else:
                    # If 'T' value is not available or empty, assign a unique identifier
                    obj_id_value = unique_id_counter
                    unique_id_counter += 1
                    value = obj_id_value

                    # Update 'T' value for the object
                    setattr(obj.boxes.id, tensor_value_attr, [value])

                cv2.putText(annotated_frame, f'Total Objects: {value}', (10, 30 + frame_object_count * 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            # Display the frame with annotated objects
            cv2.imshow("YOLOv8 Tracking", annotated_frame)
        except Exception as e:
            print("Error during YOLOv8 tracking:", e)
            break

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    else:
        # Break the loop if the end of the video is reached
        break

cap.release()
cv2.destroyAllWindows()
