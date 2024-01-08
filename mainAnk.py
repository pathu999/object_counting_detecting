import cv2
import sys
from ultralytics import YOLO
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox,QGraphicsScene,QGraphicsPixmapItem
from pyQt_ui import Ui_MainWindow  
import neoapi as npi
import tempfile
import os

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.camera = None
        self.scene = QGraphicsScene()
        self.start_view.setScene(self.scene)

        self.start_pushButton.clicked.connect(self.startcam)
        self.stop_pushButton.clicked.connect(self.stopcam)
        self.btncount.clicked.connect(self.objectcount)

    def startcam(self):
        print("Baumer camera start")
        try:
            self.camera = npi.Cam()
            self.camera.Connect()
            self.camera.f.TriggerMode = npi.TriggerMode_Off
            self.camera.f.ExposureTime.Set(260407)
        
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

                self.temp_file = tempfile.NamedTemporaryFile(suffix=".bmp", delete=False)
                self.temp_file.close()
                image.Save(self.temp_file.name)
                qimage = QImage(self.temp_file.name)
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
        pass

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
