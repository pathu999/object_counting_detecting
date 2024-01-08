# ###################################################################################################################################################################################
# import cv2
# import sys
# from ultralytics import YOLO
# from PySide6.QtCore import Qt, QTimer,QPoint
# from PySide6.QtGui import QImage, QPixmap, QPainter, QPen, QFont
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

#         self.camera_item = None

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

#                 frame = cv2.imread(temp_file.name)
#                 self.objectcount(frame)

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

#     def objectcount(self,frame):
#         self.threshold = 0.7
#         model_path = 'best.pt'
#         self.model = YOLO(model_path)
#         if self.camera is not None:
#             try:
#                 # image = self.camera.GetImage()
#                 # temp_file = tempfile.NamedTemporaryFile(suffix=".bmp", delete=False)
#                 # temp_file.close()
#                 # image.Save(temp_file.name)

#                 # frame = cv2.imread(temp_file.name)
#                 results = self.model(frame)[0]

#                 for result in results.boxes.data.tolist():
#                     x1, y1, x2, y2, score, class_id = result
#                     if score > self.threshold:
#                         cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 4)

              
#                 qimage = QImage(frame.data,frame.shape[1],frame.shape[0], frame.strides[0],QImage.Format_RGB888)
#                 pixmap = QPixmap.fromImage(qimage)
#                 self.camera_item.setPixmap(pixmap)
#                 self.start_view.fitInView(self.scene.sceneRect(), Qt.AspectRatioMode.KeepAspectRatio)
#                 print(results)
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

###########################################################################################################################################################################################################
#in this code i have achive object count in single frame 

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

        self.camera_item = None

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

                frame = cv2.imread(temp_file.name)
                self.objectcount(frame)

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

    def objectcount(self, frame):
        self.threshold = 0.7
        model_path = 'best.pt'
        self.model = YOLO(model_path)
        if self.camera is not None:
            try:
                results = self.model(frame)[0]

                unique_objects = set()  # Set to store unique detected objects

                for result in results.boxes.data.tolist():
                    x1, y1, x2, y2, score, class_id = result
                    if score > self.threshold:
                        object_id = f"{x1}-{y1}-{x2}-{y2}"  # Unique identifier for each object based on its coordinates
                        unique_objects.add(object_id)
                        cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 4)

                qimage = QImage(frame.data, frame.shape[1], frame.shape[0], frame.strides[0], QImage.Format_RGB888)
                pixmap = QPixmap.fromImage(qimage)
                self.camera_item.setPixmap(pixmap)
                self.start_view.fitInView(self.scene.sceneRect(), Qt.AspectRatioMode.KeepAspectRatio)

                # Display the count on led_number
                total_objects = len(unique_objects)
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
