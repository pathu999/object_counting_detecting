# #in this code camera connect successfully 
# import cv2
# import sys
# from ultralytics import YOLO
# from PySide6.QtCore import Qt, QTimer
# from PySide6.QtGui import QImage, QPixmap
# from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox, QGraphicsScene, QGraphicsPixmapItem
# from pyQt_ui import Ui_MainWindow  
# import neoapi as npi
# import tempfile
# import os
# from PySide6 import QtWidgets

# class MainWindow(QMainWindow, Ui_MainWindow):
#     def __init__(self):
#         super().__init__()
#         self.setupUi(self)

#         # Load YOLOv8 model
#         try:
#             self.yolo_model = YOLO('best.pt')
#         except Exception as e:
#             QMessageBox.critical(self, "Error", f"Error loading YOLOv8 model: {e}")
#             self.close()

#         self.camera = None
#         self.scene = QGraphicsScene()
#         self.start_view.setScene(self.scene)

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
#                 results = self.yolo_model(frame)

#                 # Process and display the results
#                 annotated_frame = results[0].plot()
#                 qimage = QImage(annotated_frame.data, annotated_frame.shape[1], annotated_frame.shape[0],
#                                 annotated_frame.strides[0], QImage.Format_RGB888)
#                 pixmap = QPixmap.fromImage(qimage)
#                 self.camera_item.setPixmap(pixmap)
#                 self.start_view.fitInView(self.scene.sceneRect(), Qt.AspectRatioMode.KeepAspectRatio)
                
                
#                 # Display the total count in the GUI
#                 total_objects = sum(item['count'] for item in object_info.values())
#                 self.total_objects_label = QtWidgets.QLabel(self.centralwidget)


#             except (npi.NeoException, Exception) as exc:
#                 QMessageBox.critical(self, "Error", f"Error during object detection: {exc}")
#         else:
#             QMessageBox.warning(self, "Warning", "Camera not connected.")

# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     window = MainWindow()
#     window.show()
#     sys.exit(app.exec_())

#############################################################################################

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

#                 # Display the total count in the GUI
#                 total_objects = len(results[0])
#                 QMessageBox.information(self, "Object Count", f"Total Objects: {total_objects}")

#             except (npi.NeoException, Exception) as exc:
#                 QMessageBox.critical(self, "Error", f"Error during object detection: {exc}")
#         else:
#             QMessageBox.warning(self, "Warning", "Camera not connected.")

# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     window = MainWindow()
#     window.show()
#     sys.exit(app.exec_())


######################################################################################################

import cv2
import sys
from ultralytics import YOLO
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox, QGraphicsScene, QGraphicsPixmapItem
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
        self.btncount.clicked.connect(self.objectcount)

    def startcam(self):
        print("Baumer camera start")
        try:
            self.camera = npi.Cam()
            self.camera.Connect()
            self.camera.f.TriggerMode = npi.TriggerMode_Off
            # self.camera.f.ExposureTime.Set(260407)
        
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

    def objectcount(self):
        if self.camera is not None:
            try:
                # Get the current frame from the camera feed
                image = self.camera.GetImage()
                temp_file = tempfile.NamedTemporaryFile(suffix=".bmp", delete=False)
                temp_file.close()
                image.Save(temp_file.name)

                # Read the frame using OpenCV
                frame = cv2.imread(temp_file.name)

                # Dictionary to store object counts and bounding boxes
                object_info = {}

                # Perform object detection using YOLOv8
                results = YOLO('best.pt')(frame)

                # Display the total count in the QLedNumber
                total_objects = len(results[0])
        
                self.led_number.display(total_objects)

            except (npi.NeoException, Exception) as exc:
                QMessageBox.critical(self, "Error", f"Error during object detection: {exc}")
        else:
            QMessageBox.warning(self, "Warning", "Camera not connected.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


#this part of code i want dont skip frame if user tap object count then i wont dont skip frame continue show frame and detect image 


####################################################################################################

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

#         # Initialize object-related variables
#         self.object_id_counter = 0
#         self.object_info = {}

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

#                 # Perform object detection using YOLOv8
#                 results = YOLO('best.pt')(frame)

#                 # Update object information and display the total count
#                 total_objects = self.update_object_info(results)
#                 self.led_number.display(total_objects)

#             except (npi.NeoException, Exception) as exc:
#                 QMessageBox.critical(self, "Error", f"Error during object detection: {exc}")
#         else:
#             QMessageBox.warning(self, "Warning", "Camera not connected.")

#     def update_object_info(self, results):
#         current_objects = {}
#         for result in results[0]:
#             class_id, confidence, bbox = result[0], result[1], result[2]

#             # Create a unique ID for the object
#             object_id = self.object_id_counter
#             self.object_id_counter += 1

#             # Store the object information
#             current_objects[object_id] = {
#                 'class_id': class_id,
#                 'confidence': confidence,
#                 'bbox': bbox,
#             }

#         # Update the overall object information dictionary
#         self.object_info = current_objects

#         # Return the total count of objects
#         return len(current_objects)

# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     window = MainWindow()
#     window.show()
#     sys.exit(app.exec_())
