from PySide6.QtWidgets import QGraphicsPixmapItem,QGraphicsScene,QFileDialog,QMessageBox,QInputDialog,QRadioButton
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtCore import Qt,QTimer
from datetime import datetime
from abc import ABC, abstractmethod
import neoapi as npi
import tempfile
import os

import threading
import tkinter
import numpy as np
import tempfile,inspect
from PySide6 import QtWidgets
from PySide6.QtCore import Signal,QObject
# from mvscamera.BasicDemo.CamOperation_class import CameraOperation
# from mvscamera.MvImport.MvCameraControl_class import *
import time

class camerainput(ABC):

    @abstractmethod
    def livecam(self):
        pass

    @abstractmethod
    def snap(self):
        pass

    @abstractmethod
    def triggerstop(self):
        pass

    @abstractmethod
    def triggerstart(self):
        pass

    @abstractmethod
    def saveliveimage(self):
        pass

    @abstractmethod
    def saveimage(self):
        pass

    @abstractmethod
    def addlabel(self):
        pass
    
    @abstractmethod
    def stopliveimage(self):
        pass

class Baumer(camerainput):
    def __init__(self,cameraImageViewer,inputImageViewer_2,verticalLayoutcaminput,main_window):
        self.camera = None
        self.scene = QGraphicsScene()
        self.cameraImageViewer = cameraImageViewer 
        self.main_window = main_window 
        self.cameraImageViewer.setScene(self.scene)
        self.inputImageViewer_2 = inputImageViewer_2 
        self.verticalLayoutcaminput = verticalLayoutcaminput
        self.selectedFolderName = None 

        self.save_live_timer = QTimer()
        self.save_live_timer.timeout.connect(self.capture_and_save_live_image)
      
      
    def livecam(self):
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

                self.temp_file = tempfile.NamedTemporaryFile(suffix=".bmp", delete=False)
                self.temp_file.close()
                image.Save(self.temp_file.name)
                qimage = QImage(self.temp_file.name)
                pixmap = QPixmap.fromImage(qimage)
                self.camera_item.setPixmap(pixmap)
                self.cameraImageViewer.fitInView(self.scene.sceneRect(), Qt.AspectRatioMode.KeepAspectRatio)

            except (npi.NeoException, Exception) as exc:
                print('Error: ', exc)
        else:
            print('Camera not connected.')
 
    def triggerstop(self):
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

    def triggerstart(self):
        self.camera = npi.Cam()
        self.camera.Connect()
        self.camera.f.ExposureTime.Set(260407)
        self.camera.f.TriggerMode = npi.TriggerMode_On
        self.camera.f.TriggerSource = npi.TriggerSource_Line0
        self.images_path = QFileDialog.getExistingDirectory(self.parent, "Select Image Folder")
        
      
        placeholder_pixmap = QPixmap("E:\pyqt5\demoofcamera\cameraimage.jpg")
        self.scene.clear()
        self.camera_item = QGraphicsPixmapItem(placeholder_pixmap)
        self.scene.addItem(self.camera_item)
        self.cameraImageViewer.fitInView(self.scene.sceneRect(), Qt.AspectRatioMode.KeepAspectRatio)
        self.camera.EnableImageCallback(self.capture_image_callback)

    def capture_image_callback(self, image):
        print("Received image:", image.GetImageID(),
              "Size:", image.GetSize(),
              "Height:", image.GetHeight(),
              "Width:", image.GetWidth(),
              "Pixelformat:", image.GetPixelFormat())

        if self.images_path:
            image_id = image.GetImageID()
            image_path = os.path.join(self.images_path, f"image_{image_id}.bmp")
            image.Save(image_path)
            print(f"Image saved: {image_path}") 

    def snap(self):
        screenshot = self.cameraImageViewer.grab()
        scene_2 = QGraphicsScene()
        input_item = QGraphicsPixmapItem(screenshot)
        scene_2.addItem(input_item)
        self.inputImageViewer_2.setScene(scene_2)
        self.inputImageViewer_2.fitInView(scene_2.sceneRect(), Qt.AspectRatioMode.KeepAspectRatio)

    def showSelectedFolderImage(self, folderName):
        self.selectedFolderName = folderName

    def addlabel(self):
        print('add')
        addlab = self.main_window.new_folder_path

        addlab_folder = os.path.join(addlab, "CameraInput")
        if not os.path.exists(addlab_folder):
            os.makedirs(addlab_folder)
        save_dir = addlab_folder
        
        parent_widget = self.main_window  # Replace with the appropriate parent widget

        # Get folder names from user input
        folderNames, ok = QInputDialog.getText(parent_widget, "Create Folders", "Enter folder names (comma-separated):")
        if ok:
            folderNames = folderNames.split(",")
            for folderName in folderNames:
                folderName = folderName.strip()
                radioButton = QRadioButton(folderName)
                folderPath = os.path.join(save_dir, folderName)
                os.makedirs(folderPath, exist_ok=True)
                radioButton.setObjectName(folderPath)
                radioButton.toggled.connect(lambda checked, folderPath=folderPath: self.showSelectedFolderImage(folderPath))
                self.main_window.verticalLayoutcaminput.addWidget(radioButton)

            self.main_window.verticalLayoutcaminput.addStretch()
            QMessageBox.information(parent_widget, "Folders Created", "Folders created successfully!")
      
    def saveimage(self):
        if self.selectedFolderName:
            # Generate a unique filename using current timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            image_filename = f"image_{timestamp}.png"  # Change the extension to match the image format
            
            # Get the image displayed in inputImageViewer_2
            image = self.inputImageViewer_2.scene().items()[0]  # Assuming only one item is present
            pixmap = image.pixmap()
            
            # Save the image to the selected folder
            image_path = os.path.join(self.selectedFolderName, image_filename)
            pixmap.save(image_path)

            print(f"Image saved: {image_path}")
        else:
            print("No folder selected to save the image.")

    def saveliveimage(self):
        self.save_live_timer.start(1000)  # Adjust the interval (in milliseconds) as needed

    def capture_and_save_live_image(self):
        if self.camera is not None:
            try:
                image = self.camera.GetImage()
                temp_file = tempfile.NamedTemporaryFile(suffix=".bmp", delete=False)
                temp_file.close()
                image.Save(temp_file.name)
                qimage = QImage(temp_file.name)
                pixmap = QPixmap.fromImage(qimage)

                save_dir = os.path.join(self.main_window.new_folder_path, "save_live")
                if not os.path.exists(save_dir):
                    os.makedirs(save_dir)

                image_filename = f"Image_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
                image_path = os.path.join(save_dir, image_filename)
                pixmap.save(image_path)

                print(f"Live image captured and saved successfully in {image_path}")
            except (npi.NeoException, Exception) as exc:
                print('Error capturing live image:', exc)
        else:
            print('Camera not connected.')

    def stopliveimage(self):
        self.save_live_timer.stop()
        print("Live image capture stopped.")

    

class update(QObject):
      update_pixmap_signal = Signal(QPixmap)

# class MVS(camerainput):
#     w = update()
#     def __init__(self,cameraImageViewer,inputImageViewer_2,verticalLayoutcaminput,main_window):
#         super().__init__()
#         self.camera = None
#         self.scene = QGraphicsScene()
#         self.cameraImageViewer = cameraImageViewer 
#         self.main_window = main_window 
#         self.cameraImageViewer.setScene(self.scene)
#         self.inputImageViewer_2 = inputImageViewer_2 
#         self.verticalLayoutcaminput = verticalLayoutcaminput
#         self.selectedFolderName = None

#         self.device = None
#         self.imgFolder = None
#         self.continuous_capture = False

#         self.deviceList = MV_CC_DEVICE_INFO_LIST()
#         self.tlayerType = MV_GIGE_DEVICE | MV_USB_DEVICE
#         self.cam = MvCamera()
#         self.nSelCamIndex = 0
#         self.obj_cam_operation = 0
#         self.obj_cam = 0
#         self.b_is_run = False
#         self.b_open_device=False
#         self.n_connect_num=0
#         self.b_start_grabbing = False
#         self.buf_cache = None 
#         self.st_frame_info=None
#         self.b_save_bmp=False
#         self.b_save_jpg=False
#         self.buf_save_image=None
#         self.h_thread_handle=None
#         self.model = None

#         self.scene = QGraphicsScene()
#         self.cameraImageViewer.setScene(self.scene)
        

#         self.w.update_pixmap_signal.connect(self.update_camera_pixmap)
    
#     def ToHexStr(num):
#         chaDic = {10: 'a', 11: 'b', 12: 'c', 13: 'd', 14: 'e', 15: 'f'}
#         hexStr = ""
#         if num < 0:
#             num = num + 2**32
#         while num >= 16:
#             digit = num % 16
#             hexStr = chaDic.get(digit, str(digit)) + hexStr
#             num //= 16
#         hexStr = chaDic.get(num, str(num)) + hexStr   
#         return hexStr

#     def To_hex_str(self,num):
#         chaDic = {10: 'a', 11: 'b', 12: 'c', 13: 'd', 14: 'e', 15: 'f'}
#         hexStr = ""
#         if num < 0:
#             num = num + 2**32
#         while num >= 16:
#             digit = num % 16
#             hexStr = chaDic.get(digit, str(digit)) + hexStr
#             num //= 16
#         hexStr = chaDic.get(num, str(num)) + hexStr   
#         return hexStr
    
#     def livecam(self):
#         self.deviceList = MV_CC_DEVICE_INFO_LIST()
#         ret = MvCamera.MV_CC_EnumDevices(self.tlayerType, self.deviceList)
#         if ret != 0:
#             QtWidgets.QMessageBox.showerror('Show Error', 'Enum devices fail! ret = ' + self.ToHexStr(ret))

#         if self.deviceList.nDeviceNum == 0:
#             QtWidgets.QMessageBox.showinfo('Show Info', 'Find no device!')

#         print("Find %d devices!" % self.deviceList.nDeviceNum)

#         devList = []
#         for i in range(0, self.deviceList.nDeviceNum):
#             mvcc_dev_info = cast(self.deviceList.pDeviceInfo[i], POINTER(MV_CC_DEVICE_INFO)).contents
#             if mvcc_dev_info.nTLayerType == MV_GIGE_DEVICE:
#                 print("\ngige device: [%d]" % i)
#                 strModeName = ""
#                 for per in mvcc_dev_info.SpecialInfo.stGigEInfo.chModelName:
#                     strModeName = strModeName + chr(per)
#                 print("device model name: %s" % strModeName)

#                 nip1 = ((mvcc_dev_info.SpecialInfo.stGigEInfo.nCurrentIp & 0xff000000) >> 24)
#                 nip2 = ((mvcc_dev_info.SpecialInfo.stGigEInfo.nCurrentIp & 0x00ff0000) >> 16)
#                 nip3 = ((mvcc_dev_info.SpecialInfo.stGigEInfo.nCurrentIp & 0x0000ff00) >> 8)
#                 nip4 = (mvcc_dev_info.SpecialInfo.stGigEInfo.nCurrentIp & 0x000000ff)
#                 print("current ip: %d.%d.%d.%d\n" % (nip1, nip2, nip3, nip4))
#                 devList.append("Gige[" + str(i) + "]:" + str(nip1) + "." + str(nip2) + "." + str(nip3) + "." + str(nip4))
#             elif mvcc_dev_info.nTLayerType == MV_USB_DEVICE:
#                 print("\nu3v device: [%d]" % i)
#                 strModeName = ""
#                 for per in mvcc_dev_info.SpecialInfo.stUsb3VInfo.chModelName:
#                     if per == 0:
#                         break
#                     strModeName = strModeName + chr(per)
#                 print("device model name: %s" % strModeName)

#                 strSerialNumber = ""
#                 for per in mvcc_dev_info.SpecialInfo.stUsb3VInfo.chSerialNumber:
#                     if per == 0:
#                         break
#                     strSerialNumber = strSerialNumber + chr(per)
#                 print("user serial number: %s" % strSerialNumber)
#                 devList.append("USB[" + str(i) + "]" + str(strSerialNumber))
    
#         deviceList = self.deviceList
#         nSelCamIndex = self.nSelCamIndex
#         obj_cam_operation = self.obj_cam_operation
#         b_is_run = self.b_is_run
#         cam = self.cam
#         if True == b_is_run:
#             QtWidgets.QMessageBox.showinfo('Show Info', 'Camera is Running!')
#             return
#         obj_cam_operation = CameraOperation(cam, deviceList, nSelCamIndex)
#         ret = self.open_device2(obj_cam_operation)
#         if  0!= ret:
#             b_is_run = False
#         else:
#             b_is_run = True
            
#         self.update_camera_feed()

#     def open_device2(self,obj_cam_operation):
        
#         if False == self.b_open_device:
#             nConnectionNum = int(self.n_connect_num)
#             stDeviceList = cast(obj_cam_operation.st_device_list.pDeviceInfo[nConnectionNum], POINTER(MV_CC_DEVICE_INFO)).contents
#             self.obj_cam = MvCamera()
#             ret = self.obj_cam.MV_CC_CreateHandle(stDeviceList)
#             if ret != 0:
#                 self.obj_cam.MV_CC_DestroyHandle()
#                 tkinter.messagebox.showerror('show error','create handle fail! ret = '+ self.To_hex_str(ret))
#                 return ret

#             ret = self.obj_cam.MV_CC_OpenDevice(MV_ACCESS_Exclusive, 0)
#             if ret != 0:
#                 tkinter.messagebox.showerror('show error','open device fail! ret = '+ self.To_hex_str(ret))
#                 return ret
            
#             print ("open device successfully!")
#             self.b_open_device = True
#             self.b_thread_closed = False

#             if stDeviceList.nTLayerType == MV_GIGE_DEVICE:
#                 nPacketSize = self.obj_cam.MV_CC_GetOptimalPacketSize()
#                 if int(nPacketSize) > 0:
#                     ret = self.obj_cam.MV_CC_SetIntValue("GevSCPSPacketSize",nPacketSize)
#                     if ret != 0:
#                         print ("warning: set packet size fail! ret[0x%x]" % ret)
#                 else:
#                     print ("warning: set packet size fail! ret[0x%x]" % nPacketSize)

#             stBool = c_bool(False)
#             ret =self.obj_cam.MV_CC_GetBoolValue("AcquisitionFrameRateEnable", byref(stBool))
#             if ret != 0:
#                 print ("get acquisition frame rate enable fail! ret[0x%x]" % ret)

#             stParam =  MVCC_INTVALUE()
#             memset(byref(stParam), 0, sizeof(MVCC_INTVALUE))
            
#             ret = self.obj_cam.MV_CC_GetIntValue("PayloadSize", stParam)
#             if ret != 0:
#                 print ("get payload size fail! ret[0x%x]" % ret)
#             self.n_payload_size = stParam.nCurValue
#             if None == self.buf_cache:
#                 self.buf_cache = (c_ubyte * self.n_payload_size)()

#             # ch:设置触发模式为off | en:Set trigger mode as off
#             ret = self.obj_cam.MV_CC_SetEnumValue("TriggerMode", MV_TRIGGER_MODE_OFF)
#             if ret != 0:
#                 print ("set trigger mode fail! ret[0x%x]" % ret)
#             return 0
        
#     def update_camera_feed(self):
#         if False == self.b_start_grabbing and True == self.b_open_device:
#             self.b_exit = False
#             self.b_is_run = True 

#             stParam =  MVCC_INTVALUE()
#             memset(byref(stParam), 0, sizeof(MVCC_INTVALUE))
            
#             ret = self.obj_cam.MV_CC_GetIntValue("PayloadSize", stParam)
#             if ret != 0:
#                 print ("get payload size fail! ret[0x%x]" % ret)
#                 sys.exit()
#             nPayloadSize = stParam.nCurValue

#             ret = self.obj_cam.MV_CC_StartGrabbing()
#             if ret != 0:
#                 print ("start grabbing fail! ret[0x%x]" % ret)
#                 sys.exit()
#             self.b_start_grabbing = True
#             data_buf = (c_ubyte * nPayloadSize)()

#             try:
#                 self.grabbing_thread = threading.Thread(target=self.work_thread,args=(self.obj_cam, byref(data_buf), nPayloadSize))
#                 self.grabbing_thread.start()
#             except:
#                 False == self.b_start_grabbing

#     def work_thread(self, cam=0, pData=0, nDataSize=0):
        
#         # self.lock.acquire()
#         g_bExit = False
#         stFrameInfo = MV_FRAME_OUT_INFO_EX()
#         memset(byref(stFrameInfo), 0, sizeof(stFrameInfo))
#         img_buff = None
        
#         while True:
#             ret = self.obj_cam.MV_CC_GetOneFrameTimeout(byref(self.buf_cache), self.n_payload_size, stFrameInfo, 1000)
#             if ret == 0:
             
#                 self.st_frame_info = stFrameInfo

#                 # print ("get one frame: Width[%d], Height[%d], nFrameNum[%d]"  % (self.st_frame_info.nWidth, self.st_frame_info.nHeight, self.st_frame_info.nFrameNum))
#                 self.n_save_image_size = self.st_frame_info.nWidth * self.st_frame_info.nHeight * 3 + 2048
#                 if img_buff is None:
#                     img_buff = (c_ubyte * self.n_save_image_size)()
                
#                 if True == self.b_save_jpg:
#                     self.Save_jpg()
#                 if self.buf_save_image is None:
#                     self.buf_save_image = (c_ubyte * self.n_save_image_size)()

#                 stParam = MV_SAVE_IMAGE_PARAM_EX()
#                 stParam.enImageType = MV_Image_Bmp;                                       
#                 stParam.enPixelType = self.st_frame_info.enPixelType                            
#                 stParam.nWidth      = self.st_frame_info.nWidth                                  
#                 stParam.nHeight     = self.st_frame_info.nHeight                                 
#                 stParam.nDataLen    = self.st_frame_info.nFrameLen
#                 stParam.pData       = cast(self.buf_cache, POINTER(c_ubyte))
#                 stParam.pImageBuffer =  cast(byref(self.buf_save_image), POINTER(c_ubyte)) 
#                 stParam.nBufferSize = self.n_save_image_size                               
#                 stParam.nJpgQuality     = 80;                                              
#                 if True == self.b_save_bmp:
#                     self.Save_Bmp() 
#             else:
#                 continue
         
#             stConvertParam = MV_CC_PIXEL_CONVERT_PARAM()
#             memset(byref(stConvertParam), 0, sizeof(stConvertParam))
#             stConvertParam.nWidth = self.st_frame_info.nWidth
#             stConvertParam.nHeight = self.st_frame_info.nHeight
#             stConvertParam.pSrcData = self.buf_cache
#             stConvertParam.nSrcDataLen = self.st_frame_info.nFrameLen
#             stConvertParam.enSrcPixelType = self.st_frame_info.enPixelType 

#             if PixelType_Gvsp_Mono8 == self.st_frame_info.enPixelType:
#                 numArray = MVS.Mono_numpy(self,self.buf_cache,self.st_frame_info.nWidth,self.st_frame_info.nHeight)

#             elif PixelType_Gvsp_RGB8_Packed == self.st_frame_info.enPixelType:
#                 numArray = MVS.Color_numpy(self,self.buf_cache,self.st_frame_info.nWidth,self.st_frame_info.nHeight)

#             elif  True == self.Is_mono_data(self.st_frame_info.enPixelType):
#                 nConvertSize = self.st_frame_info.nWidth * self.st_frame_info.nHeight
#                 stConvertParam.enDstPixelType = PixelType_Gvsp_Mono8
#                 stConvertParam.pDstBuffer = (c_ubyte * nConvertSize)()
#                 stConvertParam.nDstBufferSize = nConvertSize
#                 ret = self.obj_cam.MV_CC_ConvertPixelType(stConvertParam)
#                 if ret != 0:
#                     tkinter.messagebox.showerror('show error','convert pixel fail! ret = '+self.To_hex_str(ret))
#                     continue
#                 cdll.msvcrt.memcpy(byref(img_buff), stConvertParam.pDstBuffer, nConvertSize)
#                 numArray = MVS.Mono_numpy(self,img_buff,self.st_frame_info.nWidth,self.st_frame_info.nHeight)

#             elif  True == self.Is_color_data(self.st_frame_info.enPixelType):
#                 nConvertSize = self.st_frame_info.nWidth * self.st_frame_info.nHeight * 3
#                 stConvertParam.enDstPixelType = PixelType_Gvsp_RGB8_Packed
#                 stConvertParam.pDstBuffer = (c_ubyte * nConvertSize)()
#                 stConvertParam.nDstBufferSize = nConvertSize
#                 ret = self.obj_cam.MV_CC_ConvertPixelType(stConvertParam)
#                 if ret != 0:
#                     tkinter.messagebox.showerror('show error','convert pixel fail! ret = '+self.To_hex_str(ret))
#                     continue
#                 cdll.msvcrt.memcpy(byref(img_buff), stConvertParam.pDstBuffer, nConvertSize)
#                 numArray = MVS.Color_numpy(self,img_buff,self.st_frame_info.nWidth,self.st_frame_info.nHeight)

#             height, width, channel = numArray.shape
#             bytesPerLine = width * channel

#             image = QImage(numArray.data, width, height, bytesPerLine, QImage.Format_Grayscale8)
#             self.temp_file = tempfile.NamedTemporaryFile(suffix=".bmp", delete=False)
#             self.temp_file.close()
#             image.save(self.temp_file.name)
#             qimage = QImage(self.temp_file.name)
#             pixmap = QPixmap.fromImage(qimage)

#             self.w.update_pixmap_signal.emit(pixmap)
            
#     def update_camera_pixmap(self, pixmap):
#         self.scene.clear()
#         self.camera_item = QGraphicsPixmapItem()
#         self.scene.addItem(self.camera_item)
#         self.camera_item.setPixmap(pixmap)  
#         self.cameraImageViewer.fitInView(self.scene.sceneRect(), Qt.AspectRatioMode.KeepAspectRatio)

#     def Color_numpy(self,data,nWidth,nHeight):
#         data_ = np.frombuffer(data, count=int(nWidth*nHeight*3), dtype=np.uint8, offset=0)
#         data_r = data_[0:nWidth*nHeight*3:3]
#         data_g = data_[1:nWidth*nHeight*3:3]
#         data_b = data_[2:nWidth*nHeight*3:3]

#         data_r_arr = data_r.reshape(nHeight, nWidth)
#         data_g_arr = data_g.reshape(nHeight, nWidth)
#         data_b_arr = data_b.reshape(nHeight, nWidth)
#         numArray = np.zeros([nHeight, nWidth, 3],"uint8")
        
#         numArray[:, :, 2] = data_r_arr
#         numArray[:, :, 1] = data_g_arr
#         numArray[:, :, 0] = data_b_arr
#         return numArray
    
#     def Is_mono_data(self,enGvspPixelType):
#         if PixelType_Gvsp_Mono8 == enGvspPixelType or PixelType_Gvsp_Mono10 == enGvspPixelType \
#             or PixelType_Gvsp_Mono10_Packed == enGvspPixelType or PixelType_Gvsp_Mono12 == enGvspPixelType \
#             or PixelType_Gvsp_Mono12_Packed == enGvspPixelType:
#             return True
#         else:
#             return False

#     def Is_color_data(self,enGvspPixelType):
#         if PixelType_Gvsp_BayerGR8 == enGvspPixelType or PixelType_Gvsp_BayerRG8 == enGvspPixelType \
#             or PixelType_Gvsp_BayerGB8 == enGvspPixelType or PixelType_Gvsp_BayerBG8 == enGvspPixelType \
#             or PixelType_Gvsp_BayerGR10 == enGvspPixelType or PixelType_Gvsp_BayerRG10 == enGvspPixelType \
#             or PixelType_Gvsp_BayerGB10 == enGvspPixelType or PixelType_Gvsp_BayerBG10 == enGvspPixelType \
#             or PixelType_Gvsp_BayerGR12 == enGvspPixelType or PixelType_Gvsp_BayerRG12 == enGvspPixelType \
#             or PixelType_Gvsp_BayerGB12 == enGvspPixelType or PixelType_Gvsp_BayerBG12 == enGvspPixelType \
#             or PixelType_Gvsp_BayerGR10_Packed == enGvspPixelType or PixelType_Gvsp_BayerRG10_Packed == enGvspPixelType \
#             or PixelType_Gvsp_BayerGB10_Packed == enGvspPixelType or PixelType_Gvsp_BayerBG10_Packed == enGvspPixelType \
#             or PixelType_Gvsp_BayerGR12_Packed == enGvspPixelType or PixelType_Gvsp_BayerRG12_Packed== enGvspPixelType \
#             or PixelType_Gvsp_BayerGB12_Packed == enGvspPixelType or PixelType_Gvsp_BayerBG12_Packed == enGvspPixelType \
#             or PixelType_Gvsp_YUV422_Packed == enGvspPixelType or PixelType_Gvsp_YUV422_YUYV_Packed == enGvspPixelType:
#             return True
#         else:
#             return False
  
#     def Mono_numpy(self,data,nWidth,nHeight):
#         data_ = np.frombuffer(data, count=int(nWidth * nHeight), dtype=np.uint8, offset=0)
#         data_mono_arr = data_.reshape(nHeight, nWidth)
#         numArray = np.zeros([nHeight, nWidth, 1],"uint8") 
#         numArray[:, :, 0] = data_mono_arr
#         return numArray
    
#     def snap(self):
#         screenshot = self.cameraImageViewer.grab()
#         scene_2 = QGraphicsScene()
#         input_item = QGraphicsPixmapItem(screenshot)
#         scene_2.addItem(input_item)
#         self.inputImageViewer_2.setScene(scene_2)
#         self.inputImageViewer_2.fitInView(scene_2.sceneRect(), Qt.AspectRatioMode.KeepAspectRatio)

#     def triggerstop(self):
#         pass

#     def triggerstart(self):
#         pass

#     def showSelectedFolderImage(self, folderName):
#         self.selectedFolderName = folderName

#     def addlabel(self):
#         print('add')
#         addlab = self.main_window.new_folder_path

#         addlab_folder = os.path.join(addlab, "CameraInput")
#         if not os.path.exists(addlab_folder):
#             os.makedirs(addlab_folder)
#         save_dir = addlab_folder
        
#         parent_widget = self.main_window  # Replace with the appropriate parent widget

#         # Get folder names from user input
#         folderNames, ok = QInputDialog.getText(parent_widget, "Create Folders", "Enter folder names (comma-separated):")
#         if ok:
#             folderNames = folderNames.split(",")
#             for folderName in folderNames:
#                 folderName = folderName.strip()
#                 radioButton = QRadioButton(folderName)
#                 folderPath = os.path.join(save_dir, folderName)
#                 os.makedirs(folderPath, exist_ok=True)
#                 radioButton.setObjectName(folderPath)
#                 radioButton.toggled.connect(lambda checked, folderPath=folderPath: self.showSelectedFolderImage(folderPath))
#                 self.main_window.verticalLayoutcaminput.addWidget(radioButton)

#             self.main_window.verticalLayoutcaminput.addStretch()
#             QMessageBox.information(parent_widget, "Folders Created", "Folders created successfully!")
      
#     def saveimage(self):
#         if self.selectedFolderName:
#             # Generate a unique filename using current timestamp
#             timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
#             image_filename = f"image_{timestamp}.png"  # Change the extension to match the image format
            
#             # Get the image displayed in inputImageViewer_2
#             image = self.inputImageViewer_2.scene().items()[0]  # Assuming only one item is present
#             pixmap = image.pixmap()
            
#             # Save the image to the selected folder
#             image_path = os.path.join(self.selectedFolderName, image_filename)
#             pixmap.save(image_path)

#             print(f"Image saved: {image_path}")
#         else:
#             print("No folder selected to save the image.")

#     def saveliveimage(self):
#         save_dir = os.path.join(self.main_window.new_folder_path, "save_live")
#         if not os.path.exists(save_dir):
#             os.makedirs(save_dir)

#         self.continuous_capture = True  # Set flag to start continuous capture
#         image_count = 0

#         def capture_images():
#             nonlocal image_count
#             while self.continuous_capture:
#                 try:
#                     live_scene = self.cameraImageViewer.scene()

#                     # Check if the scene is not empty and has at least one item
#                     if live_scene.items():
#                         live_image = live_scene.items()[0]
#                         live_pixmap = live_image.pixmap()

#                         image_filename = f"image{image_count}.png"
#                         image_path = os.path.join(save_dir, image_filename)
#                         live_pixmap.save(image_path)

#                         print(f"Live image saved: {image_path}")

#                         image_count += 1
#                     else:
#                         print("No image found in the scene.")
#                 except Exception as e:
#                     print(f"An error occurred while saving the live image: {str(e)}")

#                 time.sleep(0.1)

#         # Create and start the thread
#         self.capture_thread = threading.Thread(target=capture_images)
#         self.capture_thread.start()

def stopliveimage(self):
        self.continuous_capture = False 
        if hasattr(self, 'capture_thread'):
            self.capture_thread.join()
        print("Live image capture stopped.")
    
