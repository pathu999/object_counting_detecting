# #in this code i have achive count object in frame after single click count button
# import cv2
# import sys
# from ultralytics import YOLO
# from PySide6.QtCore import Qt, QTimer
# from PySide6.QtGui import QImage, QPixmap
# from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox, QGraphicsScene, QGraphicsPixmapItem
# from pyQt_ui import Ui_MainWindow  
# import neoapi as npi
# import tempfile
# from threading import Thread

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
#         self.btncount.clicked.connect(self.toggle_counting)

#         self.counting_enabled = False
#         self.total_objects = 0

#     def startcam(self):
#         print("Baumer camera start")
#         try:
#             self.camera = npi.Cam()
#             self.camera.Connect()
#             self.camera.f.TriggerMode = npi.TriggerMode_Off
            
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

#                 if self.counting_enabled:
#                     self.perform_object_detection(temp_file.name)

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

#     def toggle_counting(self):
#         self.counting_enabled = not self.counting_enabled
#         if self.counting_enabled:
#             self.total_objects = 0  # Reset count when starting counting
#             self.led_number.display(self.total_objects)

#     def perform_object_detection(self, image_path):
#         try:
#             frame = cv2.imread(image_path)
#             results = YOLO('best.pt')(frame)
#             total_objects = len(results[0])
#             if total_objects > self.total_objects:
#                 self.total_objects = total_objects
#                 self.led_number.display(self.total_objects)

#         except (npi.NeoException, Exception) as exc:
#             QMessageBox.critical(self, "Error", f"Error during object detection: {exc}")

# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     window = MainWindow()
#     window.show()
#     sys.exit(app.exec_())

###########################################################################################################################
#in this part of code i have acchive count of object in frame without using count if you just start the camera then count start and  and after that we track object in single frame 
import cv2
import sys
from ultralytics import YOLO
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtWidgets import QApplication, QMainWindow, QGraphicsScene, QGraphicsPixmapItem, QMessageBox
from pyQt_ui import Ui_MainWindow  
import neoapi as npi
from threading import Thread
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
        self.total_objects = 0

        self.start_pushButton.clicked.connect(self.startcam)
        self.stop_pushButton.clicked.connect(self.stopcam)
        self.btncount.clicked.connect(self.objectcount)

    def startcam(self):
        print("Baumer camera start")
        try:
            self.camera = npi.Cam()
            self.camera.Connect()
            self.camera.f.TriggerMode = npi.TriggerMode_Off
            
            self.scene.clear()
            self.camera_item = QGraphicsPixmapItem()
            self.scene.addItem(self.camera_item)

            self.camera_timer = QTimer()
            self.camera_timer.timeout.connect(self.update_camera_feed)
            self.camera_timer.start(100) 

        except (npi.NeoException, Exception) as exc:
            print('Error: ', exc)

    def update_camera_feed(self):
        if self.camera is not None:
            try:
                image = self.camera.GetImage()

                temp_file = tempfile.NamedTemporaryFile(suffix=".bmp", delete=False)
                temp_file.close()
                image.Save(temp_file.name)
                qimage = QImage(temp_file.name)
                pixmap = QPixmap.fromImage(qimage)
                self.camera_item.setPixmap(pixmap)
                self.start_view.fitInView(self.scene.sceneRect(), Qt.AspectRatioMode.KeepAspectRatio)

                self.perform_object_detection(temp_file.name)

            except (npi.NeoException, Exception) as exc:
                print('Error: ', exc)
        else:
            print('Camera not connected.')

    def stopcam(self):
        print("Baumer camera stopped.")
        if self.camera is not None:
            try:
                self.camera_timer.stop() 
                self.camera.Disconnect()  
                self.camera = None
                self.scene.clear()
            except (npi.NeoException, Exception) as exc:
                print('Error stopping the camera:', exc)
        else:
            print('Camera not connected.')

    def perform_object_detection(self, image_path):
        try:
            frame = cv2.imread(image_path)
            results = YOLO('best.pt')(frame)
            total_objects = len(results[0])

            # Display the total count in the GUI
            self.total_objects += total_objects
            self.led_number.display(self.total_objects)

        except (npi.NeoException, Exception) as exc:
            print(f"Error during object detection: {exc}")

    def objectcount(self,frame):
        self.threshold = 0.7
        model_path = 'best.pt'
        self.model = YOLO(model_path)
        if self.camera is not None:
            try:
                # image = self.camera.GetImage()
                # temp_file = tempfile.NamedTemporaryFile(suffix=".bmp", delete=False)
                # temp_file.close()
                # image.Save(temp_file.name)

                # frame = cv2.imread(temp_file.name)
                results = self.model(frame)[0]

                for result in results.boxes.data.tolist():
                    x1, y1, x2, y2, score, class_id = result
                    if score > self.threshold:
                        cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 4)

              
                qimage = QImage(frame.data,frame.shape[1],frame.shape[0], frame.strides[0],QImage.Format_RGB888)
                pixmap = QPixmap.fromImage(qimage)
                self.camera_item.setPixmap(pixmap)
                self.start_view.fitInView(self.scene.sceneRect(), Qt.AspectRatioMode.KeepAspectRatio)
                print(results)
                # total_objects = len(results[0])
                # self.led_number.display(total_objects)

            except (npi.NeoException, Exception) as exc:
                QMessageBox.critical(self, "Error", f"Error during object detection: {exc}")
        else:
            QMessageBox.warning(self, "Warning", "Camera not connected.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

####################################################################################################################

# import cv2
# import sys
# from ultralytics import YOLO
# from PySide6.QtCore import Qt, QTimer
# from PySide6.QtGui import QImage, QPixmap
# from PySide6.QtWidgets import QApplication, QMainWindow, QGraphicsScene, QGraphicsPixmapItem, QMessageBox
# from pyQt_ui import Ui_MainWindow  
# import neoapi as npi
# from threading import Thread
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
#         self.total_objects = 0

#         self.start_pushButton.clicked.connect(self.startcam)
#         self.stop_pushButton.clicked.connect(self.stopcam)
#         self.btncount.clicked.connect(self.perform_object_detection)  # Connect to the count button

#     def startcam(self):
#         print("Baumer camera start")
#         try:
#             self.camera = npi.Cam()
#             self.camera.Connect()
#             self.camera.f.TriggerMode = npi.TriggerMode_Off
            
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

#     def perform_object_detection(self):
#         try:
#             if self.camera is not None:
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
#                 self.total_objects += total_objects
#                 self.led_number.display(self.total_objects)

#             else:
#                 QMessageBox.warning(self, "Warning", "Camera not connected.")

#         except (npi.NeoException, Exception) as exc:
#             QMessageBox.critical(self, "Error", f"Error during object detection: {exc}")

# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     window = MainWindow()
#     window.show()
#     sys.exit(app.exec_())

# import cv2
# import sys
# from ultralytics import YOLO
# from PySide6.QtCore import Qt, QTimer, QThread
# from PySide6.QtGui import QImage, QPixmap
# from PySide6.QtWidgets import QApplication, QMainWindow, QGraphicsScene, QGraphicsPixmapItem
# from pyQt_ui import Ui_MainWindow  
# import neoapi as npi
# from threading import Thread
# import tempfile

# class CameraThread(QThread):
#     def __init__(self, main_window):
#         super().__init__()
#         self.main_window = main_window

#     def run(self):
#         while self.main_window.camera is not None:
#             self.main_window.update_camera_feed()
#             # self.main_window.msleep(0)  # Adjust the sleep time as needed

# class MainWindow(QMainWindow, Ui_MainWindow):
#     def __init__(self):
#         super().__init__()
#         self.setupUi(self)

#         self.camera = None
#         self.scene = QGraphicsScene()
#         self.start_view.setScene(self.scene)

#         # Assuming that the QLedNumber widget is named ledNumber
#         self.led_number = self.count
#         self.total_objects = 0

#         self.start_pushButton.clicked.connect(self.startcam)
#         self.stop_pushButton.clicked.connect(self.stopcam)

#     def startcam(self):
#         print("Baumer camera start")
#         try:
#             self.camera = npi.Cam()
#             self.camera.Connect()
#             self.camera.f.TriggerMode = npi.TriggerMode_Off
            
#             self.scene.clear()
#             self.camera_item = QGraphicsPixmapItem()
#             self.scene.addItem(self.camera_item)

#             # Set the timer interval for 39 fps
#             self.camera_timer = QTimer()
#             self.camera_timer.timeout.connect(self.update_camera_feed)
#             self.camera_timer.start(39)  # 1000 milliseconds / 39 frames

#             # Create and start the camera thread
#             self.camera_thread = CameraThread(self)
#             self.camera_thread.start()

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

#                 self.perform_object_detection(temp_file.name)

#             except (npi.NeoException, Exception) as exc:
#                 print('Error: ', exc)
#         else:
#             print('Camera not connected.')

#     def stopcam(self):
#         print("Baumer camera stopped.")
#         if self.camera is not None:
#             try:
#                 self.camera_timer.stop() 
#                 self.camera_thread.quit()  # Stop the camera thread
#                 self.camera_thread.wait()  # Wait for the thread to finish
#                 self.camera.Disconnect()  
#                 self.camera = None
#                 self.scene.clear()
#             except (npi.NeoException, Exception) as exc:
#                 print('Error stopping the camera:', exc)
#         else:
#             print('Camera not connected.')

#     def perform_object_detection(self, image_path):
#         try:
#             frame = cv2.imread(image_path)
#             results = YOLO('best.pt')(frame)
#             total_objects = len(results[0])

#             # Display the total count in the GUI
#             self.total_objects += total_objects
#             self.led_number.display(self.total_objects)

#         except (npi.NeoException, Exception) as exc:
#             print(f"Error during object detection: {exc}")

# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     window = MainWindow()
#     window.show()
#     sys.exit(app.exec_())
###################################################################################################################
# import cv2
# from PySide6.QtCore import Qt, QTimer, QThread, Signal
# from PySide6.QtGui import QImage, QPixmap
# from PySide6.QtWidgets import QApplication, QMainWindow, QGraphicsScene, QGraphicsPixmapItem
# from pyQt_ui import Ui_MainWindow  
# import neoapi as npi
# from threading import Thread
# import tempfile
# import time
# import sys

# class CameraThread(QThread):
#     frameCaptured = Signal(object)

#     def __init__(self, main_window):
#         super().__init__()
#         self.main_window = main_window

#     def run(self):
#         while self.main_window.camera is not None:
#             try:
#                 image = self.main_window.camera.GetImage()
#                 temp_file = tempfile.NamedTemporaryFile(suffix=".bmp", delete=False)
#                 temp_file.close()
#                 image.Save(temp_file.name)
#                 self.frameCaptured.emit(temp_file.name)
#                 self.msleep(20)  # Adjust the sleep time as needed
#             except (npi.NeoException, Exception) as exc:
#                 print('Error capturing frame:', exc)

# class MainWindow(QMainWindow, Ui_MainWindow):
#     def __init__(self):
#         super().__init__()
#         self.setupUi(self)

#         self.camera = None
#         self.scene = QGraphicsScene()
#         self.start_view.setScene(self.scene)

#         # Assuming that the QLedNumber widget is named ledNumber
#         self.led_number = self.count
#         self.total_objects = 0

#         self.start_pushButton.clicked.connect(self.startcam)
#         self.stop_pushButton.clicked.connect(self.stopcam)

#         # Timestamp logic
#         self.timeout = 0.01  # 1 / FPS
#         self.old_timestamp = time.time()

#     def startcam(self):
#         print("Baumer camera start")
#         try:
#             self.camera = npi.Cam()
#             self.camera.Connect()
#             self.camera.f.TriggerMode = npi.TriggerMode_Off

#             self.scene.clear()
#             self.camera_item = QGraphicsPixmapItem()
#             self.scene.addItem(self.camera_item)

#             # Set the timer interval for 20 ms
#             self.camera_timer = QTimer()
#             self.camera_timer.timeout.connect(self.update_camera_feed)
#             self.camera_timer.start(20)

#             # Create and start the camera thread
#             self.camera_thread = CameraThread(self)
#             self.camera_thread.frameCaptured.connect(self.perform_object_detection)
#             self.camera_thread.start()

#         except (npi.NeoException, Exception) as exc:
#             print('Error: ', exc)

#     def update_camera_feed(self):
#         if self.camera is not None:
#             try:
#                 image = self.camera.GetImage()

#                 temp_file = tempfile.NamedTemporaryFile(suffix=".bmp", delete=False)
#                 temp_file.close()
#                 image.Save(temp_file.name)
#                 self.camera_item.setPixmap(QPixmap(temp_file.name))
#                 self.start_view.fitInView(self.scene.sceneRect(), Qt.AspectRatioMode.KeepAspectRatio)

#                 # Timestamp logic for displaying frames at a certain rate
#                 if (time.time() - self.old_timestamp) > self.timeout:
#                     self.perform_object_detection(temp_file.name)
#                     self.old_timestamp = time.time()

#             except (npi.NeoException, Exception) as exc:
#                 print('Error: ', exc)
#         else:
#             print('Camera not connected.')

#     def stopcam(self):
#         print("Baumer camera stopped.")
#         if self.camera is not None:
#             try:
#                 self.camera_timer.stop() 
#                 self.camera_thread.quit()  # Stop the camera thread
#                 self.camera_thread.wait()  # Wait for the thread to finish
#                 self.camera.Disconnect()  
#                 self.camera = None
#                 self.scene.clear()
#             except (npi.NeoException, Exception) as exc:
#                 print('Error stopping the camera:', exc)
#         else:
#             print('Camera not connected.')

#     def perform_object_detection(self, image_path):
#         try:
#             frame = cv2.imread(image_path)
#             results = YOLO('best.pt')(frame)
#             total_objects = len(results[0])

#             # Display the total count in the GUI
#             self.total_objects += total_objects
#             self.led_number.display(self.total_objects)

#         except (npi.NeoException, Exception) as exc:
#             print(f"Error during object detection: {exc}")

# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     window = MainWindow()
#     window.show()
#     sys.exit(app.exec_())

###############################################################################################################################
# import cv2
# import sys
# import numpy as np
# from ultralytics import YOLO
# from PySide6.QtCore import Qt, QTimer
# from PySide6.QtGui import QImage, QPixmap
# from PySide6.QtWidgets import QApplication, QMainWindow, QGraphicsScene, QGraphicsPixmapItem, QMessageBox
# from pyQt_ui import Ui_MainWindow  
# import neoapi as npi

# class MainWindow(QMainWindow, Ui_MainWindow):
#     def __init__(self):
#         super().__init__()
#         self.setupUi(self)

#         self.camera = None
#         self.scene = QGraphicsScene()
#         self.start_view.setScene(self.scene)

#         # Assuming that the QLedNumber widget is named ledNumber
#         self.led_number = self.count
#         self.total_objects = 0

#         self.start_pushButton.clicked.connect(self.startcam)
#         self.stop_pushButton.clicked.connect(self.stopcam)
#         self.btncount.clicked.connect(self.perform_object_detection)  # Connect to the count button

#     def startcam(self):
#         print("Baumer camera start")
#         try:
#             self.camera = npi.Cam()
#             self.camera.Connect()
#             self.camera.f.TriggerMode = npi.TriggerMode_Off
            
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

#                 # Convert the Baumer camera image to OpenCV format
#                 frame = self.convert_to_opencv(image)

#                 # Perform object detection using YOLOv8
#                 results = YOLO('best.pt')(frame)

#                 # Display the total count in the QLedNumber
#                 total_objects = len(results[0])
#                 self.total_objects += total_objects
#                 self.led_number.display(self.total_objects)

#                 # Display the frame in the QGraphicsView
#                 qimage = QImage(frame.data, frame.shape[1], frame.shape[0], frame.strides[0], QImage.Format_RGB888)
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

#     def perform_object_detection(self):
#         try:
#             if self.camera is not None:
#                 # Get the current frame from the camera feed
#                 image = self.camera.GetImage()

#                 # Convert the Baumer camera image to OpenCV format
#                 frame = self.convert_to_opencv(image)

#                 # Perform object detection using YOLOv8
#                 results = YOLO('best.pt')(frame)

#                 # Display the total count in the QLedNumber
#                 total_objects = len(results[0])
#                 self.total_objects += total_objects
#                 self.led_number.display(self.total_objects)

#             else:
#                 QMessageBox.warning(self, "Warning", "Camera not connected.")

#         except (npi.NeoException, Exception) as exc:
#             QMessageBox.critical(self, "Error", f"Error during object detection: {exc}")

#     def convert_to_opencv(self, camera_image):
#         try:
#             # Assuming 'get_data()' returns raw pixel data in a 1D array
#             raw_data = camera_image.get_data()

#             # Assuming the image has attributes 'get_height()' and 'get_width()'
#             height, width = camera_image.get_height(), camera_image.get_width()

#             # Reshape the 1D array to a 3D array (height x width x channels)
#             opencv_frame = np.array(raw_data).reshape((height, width, 3))

#             # If pixel values are not in the correct order, you might need to adjust them
#             # opencv_frame = cv2.cvtColor(opencv_frame, cv2.COLOR_BGR2RGB)

#             return opencv_frame

#         except Exception as e:
#             print(f"Error in convert_to_opencv: {e}")
#             return None

# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     window = MainWindow()
#     window.show()
#     sys.exit(app.exec_())
