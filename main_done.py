# import cv2
# import sys
# from ultralytics import YOLO
# from PySide6.QtCore import Qt, QTimer
# from PySide6.QtGui import QImage, QPixmap
# from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox, QGraphicsScene, QGraphicsPixmapItem
# from pyQt_ui import Ui_MainWindow  
# import neoapi as npi
# import tempfile

# class MainWindow(QMainWindow, Ui_MainWindow):
#     def __init__(self):
#         super().__init__()
#         self.setupUi(self)

#         self.camera = None
#         self.scene = QGraphicsScene()
#         self.start_view.setScene(self.scene)

#         # Assuming that the QLedNumber widget is named ledNumber
#         self.led_number = self.count
#         self.start_pushButton.clicked.connect(self.startcam)
#         self.stop_pushButton.clicked.connect(self.stopcam)
#         self.btncount.clicked.connect(self.objectcount)

#     def startcam(self):
#         print("Baumer camera start")
#         try:
#             self.camera = npi.Cam()
#             self.camera.Connect()
#             self.camera.f.TriggerMode = npi.TriggerMode_Off
#             self.camera.f.ExposureTime.Set(260407)
        
#             self.scene.clear()
#             self.camera_item = QGraphicsPixmapItem()
#             self.scene.addItem(self.camera_item)
#             self.camera_timer = QTimer()
#             self.camera_timer.timeout.connect(self.update_camera_feed)
#             self.camera_timer.start(100) 
#         except (npi.NeoException, Exception) as exc:
#             print('Error: ', exc)
    
#     def update_camera_feed(self):
#         if self.camera is not None:
#             try:
#                 image = self.camera.GetImage()

#                 temp_file = tempfile.NamedTemporaryFile(suffix=".bmp", delete=False)
#                 temp_file.close()
#                 image.Save(temp_file.name)
#                 qimage = QImage(temp_file.name)
#                 pixmap = QPixmap.fromImage(qimage)
#                 self.camera_item.setPixmap(pixmap)
#                 self.start_view.fitInView(self.scene.sceneRect(), Qt.AspectRatioMode.KeepAspectRatio)

#             except (npi.NeoException, Exception) as exc:
#                 print('Error: ', exc)
#         else:
#             print('Camera not connected.')
    
#     def stopcam(self):
#         print("Baumer camera stopped.")
#         if self.camera is not None:
#             try:
#                 self.camera_timer.stop() 
#                 self.camera.Disconnect()  
#                 self.camera = None
#                 self.scene.clear()
#             except (npi.NeoException, Exception) as exc:
#                 print('Error stopping the camera:', exc)
#         else:
#             print('Camera not connected.')

#     def objectcount(self):
#         if self.camera is not None:
#             try:
#                 # Get the current frame from the camera feed
#                 image = self.camera.GetImage()
#                 temp_file = tempfile.NamedTemporaryFile(suffix=".bmp", delete=False)
#                 temp_file.close()
#                 image.Save(temp_file.name)

#                 # Read the frame using OpenCV
#                 frame = cv2.imread(temp_file.name)

#                 # Dictionary to store object counts and bounding boxes
#                 object_info = {}

#                 # Perform object detection using YOLOv8
#                 results = YOLO('best.pt')(frame)

#                 # Display the total count in the QLedNumber
#                 total_objects = len(results[0])
#                 self.led_number.display(total_objects)

#             except (npi.NeoException, Exception) as exc:
#                 QMessageBox.critical(self, "Error", f"Error during object detection: {exc}")
#         else:
#             QMessageBox.warning(self, "Warning", "Camera not connected.")

# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     window = MainWindow()
#     window.show()
#     sys.exit(app.exec_())

###################################################################################################################
#in this code i have achive object_count in frame 
# import cv2
# import sys
# from ultralytics import YOLO
# from PySide6.QtCore import Qt, QTimer
# from PySide6.QtGui import QImage, QPixmap
# from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox, QGraphicsScene, QGraphicsPixmapItem
# from pyQt_ui import Ui_MainWindow  
# import neoapi as npi
# import tempfile

# class MainWindow(QMainWindow, Ui_MainWindow):
#     def __init__(self):
#         super().__init__()
#         self.setupUi(self)

#         self.camera = None
#         self.scene = QGraphicsScene()
#         self.start_view.setScene(self.scene)

#         # Assuming that the QLedNumber widget is named ledNumber
#         self.led_number = self.count
#         self.start_pushButton.clicked.connect(self.startcam)
#         self.stop_pushButton.clicked.connect(self.stopcam)
#         self.btncount.clicked.connect(self.start_object_detection)

#         # List to store object counts
#         self.object_counts = []

#         # Timer for object detection
#         self.object_detection_timer = QTimer(self)
#         self.object_detection_timer.timeout.connect(self.objectcount)

#     def startcam(self):
#         print("Baumer camera start")
#         try:
#             self.camera = npi.Cam()
#             self.camera.Connect()
#             self.camera.f.TriggerMode = npi.TriggerMode_Off
#             self.camera.f.ExposureTime.Set(260407)
        
#             self.scene.clear()
#             self.camera_item = QGraphicsPixmapItem()
#             self.scene.addItem(self.camera_item)
#             self.camera_timer = QTimer()
#             self.camera_timer.timeout.connect(self.update_camera_feed)
#             self.camera_timer.start(100) 
#         except (npi.NeoException, Exception) as exc:
#             print('Error: ', exc)

#     def start_object_detection(self):
#         # Start the timer for object detection
#         self.object_detection_timer.start(1000)  # Set the interval (in milliseconds)

#     def update_camera_feed(self):
#         if self.camera is not None:
#             try:
#                 image = self.camera.GetImage()

#                 temp_file = tempfile.NamedTemporaryFile(suffix=".bmp", delete=False)
#                 temp_file.close()
#                 image.Save(temp_file.name)
#                 qimage = QImage(temp_file.name)
#                 pixmap = QPixmap.fromImage(qimage)
#                 self.camera_item.setPixmap(pixmap)
#                 self.start_view.fitInView(self.scene.sceneRect(), Qt.AspectRatioMode.KeepAspectRatio)

#             except (npi.NeoException, Exception) as exc:
#                 print('Error: ', exc)
#         else:
#             print('Camera not connected.')

#     def stopcam(self):
#         print("Baumer camera stopped.")
#         if self.camera is not None:
#             try:
#                 self.camera_timer.stop() 
#                 self.object_detection_timer.stop()  # Stop the object detection timer
#                 self.camera.Disconnect()  
#                 self.camera = None
#                 self.scene.clear()
#             except (npi.NeoException, Exception) as exc:
#                 print('Error stopping the camera:', exc)
#         else:
#             print('Camera not connected.')

#     def objectcount(self):
#         if self.camera is not None:
#             try:
#                 # Get the current frame from the camera feed
#                 image = self.camera.GetImage()
#                 temp_file = tempfile.NamedTemporaryFile(suffix=".bmp", delete=False)
#                 temp_file.close()
#                 image.Save(temp_file.name)

#                 # Read the frame using OpenCV
#                 frame = cv2.imread(temp_file.name)

#                 # Dictionary to store object counts and bounding boxes
#                 object_info = {}

#                 # Perform object detection using YOLOv8
#                 results = YOLO('best.pt')(frame)

#                 # Display the total count in the QLedNumber
#                 total_objects = len(results[0])
#                 self.led_number.display(total_objects)

#                 # Append the object count to the list
#                 self.object_counts.append(total_objects)

#             except (npi.NeoException, Exception) as exc:
#                 QMessageBox.critical(self, "Error", f"Error during object detection: {exc}")
#         else:
#             QMessageBox.warning(self, "Warning", "Camera not connected.")

# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     window = MainWindow()
#     window.show()
#     sys.exit(app.exec_())

########################################################################################################
# import cv2
# import sys
# from ultralytics import YOLO
# from PySide6.QtCore import Qt, QTimer
# from PySide6.QtGui import QImage, QPixmap
# from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox, QGraphicsScene, QGraphicsPixmapItem
# from pyQt_ui import Ui_MainWindow  
# import neoapi as npi
# import tempfile

# class MainWindow(QMainWindow, Ui_MainWindow):
#     def __init__(self):
#         super().__init__()
#         self.setupUi(self)

#         self.camera = None
#         self.scene = QGraphicsScene()
#         self.start_view.setScene(self.scene)

#         # Assuming that the QLedNumber widget is named ledNumber
#         self.led_number = self.count
#         self.start_pushButton.clicked.connect(self.startcam)
#         self.stop_pushButton.clicked.connect(self.stopcam)
#         self.btncount.clicked.connect(self.start_object_detection)

#         # List to store total object counts
#         self.total_object_counts = []

#         # Timer for object detection
#         self.object_detection_timer = QTimer(self)
#         self.object_detection_timer.timeout.connect(self.objectcount)

#     def startcam(self):
#         print("Baumer camera start")
#         try:
#             self.camera = npi.Cam()
#             self.camera.Connect()

#             # Increase shutter speed (adjust the value accordingly)
#             self.camera.f.TriggerMode = npi.TriggerMode_Off
#             self.camera.f.ExposureTime.Set(100000)  # Adjust this value as needed
        
#             self.scene.clear()
#             self.camera_item = QGraphicsPixmapItem()
#             self.scene.addItem(self.camera_item)
#             self.camera_timer = QTimer()
#             self.camera_timer.timeout.connect(self.update_camera_feed)
#             self.camera_timer.start(100) 
#         except (npi.NeoException, Exception) as exc:
#             print('Error: ', exc)

#     def start_object_detection(self):
#         # Start the timer for object detection
#         self.object_detection_timer.start(1000)  # Set the interval (in milliseconds)

#     def update_camera_feed(self):
#         if self.camera is not None:
#             try:
#                 image = self.camera.GetImage()

#                 temp_file = tempfile.NamedTemporaryFile(suffix=".bmp", delete=False)
#                 temp_file.close()
#                 image.Save(temp_file.name)
#                 qimage = QImage(temp_file.name)
#                 pixmap = QPixmap.fromImage(qimage)
#                 self.camera_item.setPixmap(pixmap)
#                 self.start_view.fitInView(self.scene.sceneRect(), Qt.AspectRatioMode.KeepAspectRatio)

#             except (npi.NeoException, Exception) as exc:
#                 print('Error: ', exc)
#         else:
#             print('Camera not connected.')

#     def stopcam(self):
#         print("Baumer camera stopped.")
#         if self.camera is not None:
#             try:
#                 self.camera_timer.stop() 
#                 self.object_detection_timer.stop()  # Stop the object detection timer
#                 self.camera.Disconnect()  
#                 self.camera = None
#                 self.scene.clear()
#             except (npi.NeoException, Exception) as exc:
#                 print('Error stopping the camera:', exc)
#         else:
#             print('Camera not connected.')

#     def objectcount(self):
#         if self.camera is not None:
#             try:
#                 # Get the current frame from the camera feed
#                 image = self.camera.GetImage()
#                 temp_file = tempfile.NamedTemporaryFile(suffix=".bmp", delete=False)
#                 temp_file.close()
#                 image.Save(temp_file.name)

#                 # Read the frame using OpenCV
#                 frame = cv2.imread(temp_file.name)

#                 # Perform object detection using YOLOv8
#                 results = YOLO('best.pt')(frame)

#                 # Display the total count in the QLedNumber
#                 total_objects = len(results[0])
#                 self.led_number.display(total_objects)

#                 # Append the total object count to the list
#                 self.total_object_counts.append(total_objects)

#             except (npi.NeoException, Exception) as exc:
#                 QMessageBox.critical(self, "Error", f"Error during object detection: {exc}")
#         else:
#             QMessageBox.warning(self, "Warning", "Camera not connected.")

# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     window = MainWindow()
#     window.show()
#     sys.exit(app.exec_())

#######################################################################################################
# import cv2
# import sys
# from ultralytics import YOLO
# from PySide6.QtCore import Qt, QTimer
# from PySide6.QtGui import QImage, QPixmap
# from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox, QGraphicsScene, QGraphicsPixmapItem
# from pyQt_ui import Ui_MainWindow  
# import neoapi as npi
# import tempfile

# class MainWindow(QMainWindow, Ui_MainWindow):
#     def __init__(self):
#         super().__init__()
#         self.setupUi(self)

#         self.camera = None
#         self.scene = QGraphicsScene()
#         self.start_view.setScene(self.scene)

#         # Assuming that the QLedNumber widget is named ledNumber
#         self.led_number = self.count
#         self.start_pushButton.clicked.connect(self.startcam)
#         self.stop_pushButton.clicked.connect(self.stopcam)
#         self.btncount.clicked.connect(self.start_object_detection)
#         self.total_count_button.connect(self.total_count_obj)
#         # List to store total object counts
#         self.total_object_counts = []

#         # Timer for object detection
#         self.object_detection_timer = QTimer(self)
#         self.object_detection_timer.timeout.connect(self.objectcount)

#     def startcam(self):
#         print("Baumer camera start")
#         try:
#             self.camera = npi.Cam()
#             self.camera.Connect()

#             # Increase shutter speed (adjust the value accordingly)
#             shutter_speed = 100000  # Adjust this value as needed
#             self.camera.f.TriggerMode = npi.TriggerMode_Off
#             self.camera.f.ExposureTime.Set(shutter_speed)

#             self.scene.clear()
#             self.camera_item = QGraphicsPixmapItem()
#             self.scene.addItem(self.camera_item)

#             # Adjust the timer interval for a smoother live feed
#             camera_update_interval = 50  # Set the interval (in milliseconds)
#             self.camera_timer = QTimer()
#             self.camera_timer.timeout.connect(self.update_camera_feed)
#             self.camera_timer.start(camera_update_interval)  # Adjust this value based on the desired frame update frequency
#         except (npi.NeoException, Exception) as exc:
#             print('Error: ', exc)

#     def start_object_detection(self):
#         # Start the timer for object detection
#         object_detection_interval = 1000  # Set the interval (in milliseconds)
#         self.object_detection_timer.start(object_detection_interval)

#     def update_camera_feed(self):
#         if self.camera is not None:
#             try:
#                 image = self.camera.GetImage()

#                 with tempfile.NamedTemporaryFile(suffix=".bmp", delete=False) as temp_file:
#                     temp_file.close()
#                     image.Save(temp_file.name)
#                     qimage = QImage(temp_file.name)
#                     pixmap = QPixmap.fromImage(qimage)
#                     self.camera_item.setPixmap(pixmap)
#                     self.start_view.fitInView(self.scene.sceneRect(), Qt.AspectRatioMode.KeepAspectRatio)

#             except (npi.NeoException, Exception) as exc:
#                 print('Error: ', exc)
#         else:
#             print('Camera not connected.')

#     def stopcam(self):
#         print("Baumer camera stopped.")
#         if self.camera is not None:
#             try:
#                 self.camera_timer.stop() 
#                 self.object_detection_timer.stop()  # Stop the object detection timer
#                 self.camera.Disconnect()  
#                 self.camera = None
#                 self.scene.clear()
#             except (npi.NeoException, Exception) as exc:
#                 print('Error stopping the camera:', exc)
#         else:
#             print('Camera not connected.')

#     def objectcount(self):
#         if self.camera is not None:
#             try:
#                 # Get the current frame from the camera feed
#                 image = self.camera.GetImage()
#                 with tempfile.NamedTemporaryFile(suffix=".bmp", delete=False) as temp_file:
#                     temp_file.close()
#                     image.Save(temp_file.name)

#                     # Read the frame using OpenCV
#                     frame = cv2.imread(temp_file.name)

#                     # Perform object detection using YOLOv8
#                     results = YOLO('best.pt')(frame)

#                     # Display the total count in the QLedNumber
#                     total_objects = len(results[0])
#                     self.led_number.display(total_objects)

#                     # Append the total object count to the list
#                     self.total_object_counts.append(total_objects)

#             except (npi.NeoException, Exception) as exc:
#                 QMessageBox.critical(self, "Error", f"Error during object detection: {exc}")
#         else:
#             QMessageBox.warning(self, "Warning", "Camera not connected.")
#     def total_count_obj(self):
#         pass


# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     window = MainWindow()
#     window.show()
#     sys.exit(app.exec_())

#####################################################################################################################

import cv2
import sys
from yolov8 import detect  # Assuming you have a yolov8 module for detection
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QImage, QPixmap, QPainter, QPen
from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox, QGraphicsScene, QGraphicsPixmapItem, QTextEdit
from pyQt_ui import Ui_MainWindow
import neoapi as npi
import tempfile

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.camera = None
        self.scene = QGraphicsScene()
        self.start_view.setScene(self.scene)

        # Assuming that the QLedNumber widget is named ledNumber
        self.led_number = self.count
        self.start_pushButton.clicked.connect(self.startcam)
        self.stop_pushButton.clicked.connect(self.stopcam)
        self.btncount.clicked.connect(self.start_object_detection)
        self.total_count_button.clicked.connect(self.total_count_obj)
        # List to store total object counts
        self.total_object_counts = []

        # Timer for object detection
        self.object_detection_timer = QTimer(self)
        self.object_detection_timer.timeout.connect(self.objectcount)

        # Counter for assigning unique IDs to detected objects
        self.object_id_counter = 0

    def startcam(self):
        print("Baumer camera start")
        try:
            self.camera = npi.Cam()
            self.camera.Connect()

            # Increase shutter speed (adjust the value accordingly)
            shutter_speed = 100000  # Adjust this value as needed
            self.camera.f.TriggerMode = npi.TriggerMode_Off
            self.camera.f.ExposureTime.Set(shutter_speed)

            self.scene.clear()
            self.camera_item = QGraphicsPixmapItem()
            self.scene.addItem(self.camera_item)

            # Adjust the timer interval for a smoother live feed
            camera_update_interval = 50  # Set the interval (in milliseconds)
            self.camera_timer = QTimer()
            self.camera_timer.timeout.connect(self.update_camera_feed)
            self.camera_timer.start(camera_update_interval)  # Adjust this value based on the desired frame update frequency
        except (npi.NeoException, Exception) as exc:
            print('Error: ', exc)

    def start_object_detection(self):
        # Start the timer for object detection
        object_detection_interval = 1000  # Set the interval (in milliseconds)
        self.object_detection_timer.start(object_detection_interval)

    def update_camera_feed(self):
        if self.camera is not None:
            try:
                image = self.camera.GetImage()

                with tempfile.NamedTemporaryFile(suffix=".bmp", delete=False) as temp_file:
                    temp_file.close()
                    image.Save(temp_file.name)
                    qimage = QImage(temp_file.name)
                    pixmap = QPixmap.fromImage(qimage)
                    self.camera_item.setPixmap(pixmap)
                    self.start_view.fitInView(self.scene.sceneRect(), Qt.AspectRatioMode.KeepAspectRatio)

            except (npi.NeoException, Exception) as exc:
                print('Error: ', exc)
        else:
            print('Camera not connected.')

    def stopcam(self):
        print("Baumer camera stopped.")
        if self.camera is not None:
            try:
                self.camera_timer.stop() 
                self.object_detection_timer.stop()  # Stop the object detection timer
                self.camera.Disconnect()  
                self.camera = None
                self.scene.clear()
            except (npi.NeoException, Exception) as exc:
                print('Error stopping the camera:', exc)
        else:
            print('Camera not connected.')

    def objectcount(self):
        if self.camera is not None:
            try:
                # Get the current frame from the camera feed
                image = self.camera.GetImage()
                with tempfile.NamedTemporaryFile(suffix=".bmp", delete=False) as temp_file:
                    temp_file.close()
                    image.Save(temp_file.name)

                    # Read the frame using OpenCV
                    frame = cv2.imread(temp_file.name)

                    # Perform object detection using YOLOv8
                    results = detect(frame, 'yolov8.cfg', 'yolov8.weights', 'coco.names')

                    # Display the total count in the QLedNumber
                    total_objects = len(results)
                    self.led_number.display(total_objects)

                    # Append the total object count to the list
                    self.total_object_counts.append(total_objects)

                    # Draw bounding boxes on the image
                    self.draw_bounding_boxes(frame, results)

            except (npi.NeoException, Exception) as exc:
                QMessageBox.critical(self, "Error", f"Error during object detection: {exc}")
        else:
            QMessageBox.warning(self, "Warning", "Camera not connected.")

    def draw_bounding_boxes(self, image, results):
        # Draw bounding boxes on the image using OpenCV
        for result in results:
            x, y, w, h = result['box']
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Convert the image to QImage and display in the QGraphicsView
        height, width, channel = image.shape
        bytes_per_line = 3 * width
        qimage = QImage(image.data, width, height, bytes_per_line, QImage.Format_RGB888).rgbSwapped()
        pixmap = QPixmap.fromImage(qimage)
        self.camera_item.setPixmap(pixmap)

    def total_count_obj(self):
        if self.camera is not None:
            try:
                # Get the current frame from the camera feed
                image = self.camera.GetImage()
                with tempfile.NamedTemporaryFile(suffix=".bmp", delete=False) as temp_file:
                    temp_file.close()
                    image.Save(temp_file.name)

                    # Read the frame using OpenCV
                    frame = cv2.imread(temp_file.name)

                    # Perform object detection using YOLOv8
                    results = detect(frame, 'yolov8.cfg', 'yolov8.weights', 'coco.names')

                    # Process individual objects and assign IDs
                    for obj in results:
                        # Increment the ID counter
                        self.object_id_counter += 1

                        # Display the ID and class label in the QTextEdit
                        self.total_count_2.append(f"Object ID: {self.object_id_counter}, Class: {obj['class']}")

                        # Draw bounding box on the image
                        x, y, w, h = obj['box']
                        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

                    # Convert the image to QImage and display in the QGraphicsView
                    height, width, channel = frame.shape
                    bytes_per_line = 3 * width
                    qimage = QImage(frame.data, width, height, bytes_per_line, QImage.Format_RGB888).rgbSwapped()
                    pixmap = QPixmap.fromImage(qimage)
                    self.camera_item.setPixmap(pixmap)

            except (npi.NeoException, Exception) as exc:
                QMessageBox.critical(self, "Error", f"Error during object counting: {exc}")
        else:
            QMessageBox.warning(self, "Warning", "Camera not connected.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
