import cv2
import sys
from ultralytics import YOLO
from PySide6.QtCore import Qt, QTimer, QObject, Signal
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtWidgets import QApplication, QMainWindow, QGraphicsScene, QGraphicsPixmapItem
from pyQt_ui import Ui_MainWindow  
import neoapi as npi
from threading import Thread
import tempfile
import time

class VideoProcessor(QObject):
    frame_processed = Signal(QImage, int)

    def __init__(self, video_path, parent=None):
        super().__init__(parent)
        self.video_path = video_path
        self.cap = cv2.VideoCapture(video_path)
        self.running = False
        self.previous_frame = None
        self.detected_objects = set()

    def start_processing(self):
        self.running = True
        while self.running:
            try:
                ret, frame = self.cap.read()
                if not ret:
                    break

                # Process frame
                qimage = self.convert_frame_to_qimage(frame)
                total_objects = self.perform_object_detection(frame)

                # Emit the frame and total_objects
                self.frame_processed.emit(qimage, total_objects)

            except Exception as exc:
                print('Error: ', exc)

        self.cap.release()

    def stop_processing(self):
        self.running = False

    def convert_frame_to_qimage(self, frame):
        height, width, channel = frame.shape
        bytes_per_line = 3 * width
        qimage = QImage(frame.data, width, height, bytes_per_line, QImage.Format_RGB888).rgbSwapped()
        return qimage

    def perform_object_detection(self, frame):
        try:
            results = YOLO('best.pt')(frame)
            total_objects = self.count_objects(results)
            return total_objects
        except Exception as exc:
            print(f"Error during object detection: {exc}")
            return 0

    def count_objects(self, results):
        current_frame = set([(obj[4], obj[0]) for obj in results[0]])

        if self.previous_frame is not None:
            new_objects = current_frame.difference(self.previous_frame)
            self.detected_objects.update(new_objects)

        total_objects = len(self.detected_objects)
        self.previous_frame = current_frame

        return total_objects


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.video_path = r"D:\Prathamesh_Data\object_count_camera_Baumer\10_brass_ring.mp4"  # Replace with the path to your video file
        self.scene = QGraphicsScene()
        self.start_view.setScene(self.scene)

        self.led_number = self.count
        self.total_objects = 0

        self.start_pushButton.clicked.connect(self.start_processing)
        self.stop_pushButton.clicked.connect(self.stop_processing)

        self.video_processor = None
        self.video_thread = None
        self.camera_item = QGraphicsPixmapItem()  # Add this line to create the QGraphicsPixmapItem

    def start_processing(self):
        print("Video processing start")
        try:
            self.scene.clear()
            self.scene.addItem(self.camera_item)  # Add this line to add the item to the scene
            self.video_processor = VideoProcessor(self.video_path)
            self.video_processor.frame_processed.connect(self.update_camera_feed)

            self.video_thread = Thread(target=self.video_processor.start_processing)
            self.video_thread.start()

        except Exception as exc:
            print('Error: ', exc)

    def update_camera_feed(self, qimage, total_objects):
        pixmap = QPixmap.fromImage(qimage)
        self.camera_item.setPixmap(pixmap)
        self.start_view.fitInView(self.scene.sceneRect(), Qt.AspectRatioMode.KeepAspectRatio)

        self.total_objects = total_objects
        self.led_number.display(self.total_objects)

    def stop_processing(self):
        print("Video processing stopped.")
        if self.video_processor is not None:
            self.video_processor.stop_processing()
            self.video_thread.join()  # Wait for the thread to finish

        self.scene.clear()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
