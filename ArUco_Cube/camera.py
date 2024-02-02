# Copyright (C) 2023 The Qt Company Ltd.
# SPDX-License-Identifier: LicenseRef-Qt-Commercial OR BSD-3-Clause

import os
from pathlib import Path
import time

from PySide6.QtMultimedia import (QAudioInput, QCamera, QCameraDevice,
                                  QImageCapture, QMediaCaptureSession,
                                  QMediaDevices, QMediaMetaData,
                                  QMediaRecorder)
from PySide6.QtWidgets import QDialog, QMainWindow, QMessageBox, QApplication as qApp
from PySide6.QtGui import QAction, QActionGroup, QIcon, QImage, QPixmap, QPainter, QFont, QColor
from PySide6.QtCore import QDateTime, QDir, QTimer, Qt, Slot, qWarning,QRect
from PySide6.QtWidgets import (QApplication, QCheckBox, QFrame, QGridLayout,
    QLabel, QMainWindow, QMenu, QMenuBar,
    QPushButton, QSizePolicy, QSlider, QSpacerItem,
    QStackedWidget, QStatusBar, QWidget)
from metadatadialog import MetaDataDialog
from PySide6.QtMultimediaWidgets import QVideoWidget
from imagesettings import ImageSettings
from videosettings import VideoSettings
from PySide6.QtWidgets import QMainWindow, QApplication

from ui_camera import Ui_Camera
# ArUco Imports
import numpy as np
import cv2, PIL, os
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import matplotlib as mpl
import pandas as pd


from calibration import start_calibration

class Camera(QMainWindow):
    def __init__(self):
        super().__init__()

        self._video_devices_group = None
        self.m_devices = QMediaDevices()
        self.m_imageCapture = None
        self.m_captureSession = QMediaCaptureSession()
        self.m_camera = None
        self.m_mediaRecorder = None

        self.m_isCapturingImage = False
        self.m_applicationExiting = False
        self.m_doImageCapture = True

        self.m_metaDataDialog = None

        self._ui = Ui_Camera()
        self._ui.setupUi(self)
        image = os.path.join(Path(__file__).parent, "shutter.svg")
        self._ui.takeImageButton.setIcon(QIcon(os.fspath(image)))
        self._ui.actionAbout_Qt.triggered.connect(qApp.aboutQt)

        # disable all buttons by default
        self.updateCameraActive(False)
        self.readyForCapture(False)

        # try to actually initialize camera & mic

        self.initialize()



    @Slot()
    def initialize(self):
        self.m_audioInput = QAudioInput()
        self.m_captureSession.setAudioInput(self.m_audioInput)

        # Camera devices

        self._video_devices_group = QActionGroup(self)
        self._video_devices_group.setExclusive(True)
        self.updateCameras()
        self.m_devices.videoInputsChanged.connect(self.updateCameras)

        self._video_devices_group.triggered.connect(self.updateCameraDevice)
        self._ui.captureWidget.currentChanged.connect(self.updateCaptureMode)

        self._ui.exposureCompensation.valueChanged.connect(self.setExposureCompensation)

        self.setCamera(QMediaDevices.defaultVideoInput())

    @Slot(QCameraDevice)
    def setCamera(self, cameraDevice):
        self.m_camera = QCamera(cameraDevice)
        self.m_captureSession.setCamera(self.m_camera)

        self.m_camera.activeChanged.connect(self.updateCameraActive)
        self.m_camera.errorOccurred.connect(self.displayCameraError)

        if not self.m_mediaRecorder:
            self.m_mediaRecorder = QMediaRecorder()
            self.m_captureSession.setRecorder(self.m_mediaRecorder)
            #self.m_mediaRecorder.recorderStateChanged.connect(self.updateRecorderState)
            self.m_mediaRecorder.durationChanged.connect(self.updateRecordTime)
            self.m_mediaRecorder.errorChanged.connect(self.displayRecorderError)

        if not self.m_imageCapture:
            self.m_imageCapture = QImageCapture()
            self.m_captureSession.setImageCapture(self.m_imageCapture)
            self.m_imageCapture.readyForCaptureChanged.connect(self.readyForCapture)
            self.m_captureSession.setImageCapture(self.m_imageCapture)
            self.m_imageCapture.imageCaptured.connect(self.processCapturedImage)
            self.m_imageCapture.imageCaptured.connect(self.imageCapturedText)
            self.m_imageCapture.imageSaved.connect(self.imageSaved)
            self.m_imageCapture.errorOccurred.connect(self.displayCaptureError)

        self.m_captureSession.setVideoOutput(self._ui.viewfinder)

        self.updateCameraActive(self.m_camera.isActive())
        #self.updateRecorderState(self.m_mediaRecorder.recorderState())
        self.readyForCapture(self.m_imageCapture.isReadyForCapture())
        self.updateCaptureMode()
        self.m_camera.start()
         # Create a QTimer to trigger the capture at regular intervals (e.g., every second)
        self.loop = False
        # Define the calibration varibales
        self.calibration = False
        self.countCalibrate = 1
        # Define the number of photos that you want
        self.numPhotosCalibrate = 10
        # Define the delay between each photo
        self.delayPhotos = 1000
        """self.timer = QTimer(self.m_camera)
        self.timer.timeout.connect(self.captureFrameLoop)
        self.timer.start(20) 
        """
        
    def keyPressEvent(self, event):
        if event.isAutoRepeat():
            return

        key = event.key()
        if key == Qt.Key_CameraFocus:
            self.displayViewfinder()
            event.accept()
        elif key == Qt.Key_Camera:
            if self.m_doImageCapture:
                self.takeImage()
            else:
                if self.m_mediaRecorder.recorderState() == QMediaRecorder.RecordingState:
                    self.stop()
                else:
                    self.record()

            event.accept()
        else:
            super().keyPressEvent(event)
     
    @Slot()
    def captureFrameLoop(self):
        # Slot to handle frame capture
        if (not self.loop):
            self.loop= True
            self.timerLoop =  QTimer(self.m_camera)
            self.timerLoop.timeout.connect(self.captureFrameLoop)
            self.timerLoop.start(20) 
            
        self.m_imageCapture.capture() 
            
    @Slot()
    def imageCapturedText(self, requestId, image):
        # Slot to handle captured images
        # Add text to the image
        if (self.loop):
            scaled_image = image.scaled(self._ui.viewfinder.size(), Qt.KeepAspectRatio,
                                    Qt.SmoothTransformation)
            image_with_text = self.addTextToImage(scaled_image, "Hello, World!")

            # Display the modified image
            self._ui.lastImagePreviewLabel.setPixmap(QPixmap.fromImage(image_with_text))

            # Display captured image for 4 seconds.
            self.displayCapturedImage()
        
    @Slot()
    def addTextToImage(self, image, text):
        # Create a QPixmap from the QImage
        pixmap = QPixmap.fromImage(image)

        # Create a QPainter to draw on the image
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)

        # Set font and color for the overlay text
        font = QFont("Arial", 16)
        color = QColor("white")
        painter.setFont(font)
        painter.setPen(color)

        # Draw the overlay text at the bottom of the image
        painter.drawText(pixmap.rect(), Qt.AlignTop| Qt.AlignHCenter, text)

        # End painting
        painter.end()

        # Convert the QPixmap back to a QImage
        modified_image = pixmap.toImage()

        return modified_image


    @Slot()
    def calibrate(self):
        """ self.calibration = True
        self.timer = QTimer(self.m_camera)
        self.timer.timeout.connect(self.takeImage)
        # Define the time to take x photos in miliseconds
        self.timer.start(self.delayPhotos) """
        dir = "c:/Users/mirko/Documents/Studium/Master/Semester05/3D_Mocap/3DSMC_Project/ArUco_Cube/images/"
        #_, mtx, _, _, _ = start_calibration(os.path.join(os.path.dirname(__file__), "images"))
        _, mtx, _, _, _ = start_calibration(dir)
        print("CALIBRATION MATRIX: ", mtx)

    @Slot()
    def updateRecordTime(self):
        d = self.m_mediaRecorder.duration() / 1000
        self._ui.statusbar.showMessage(f"Recorded {d} sec")

    @Slot(int, QImage)
    def processCapturedImage(self, requestId, img):
        if self.m_isCapturingImage:
            scaled_image = img.scaled(self._ui.viewfinder.size(), Qt.KeepAspectRatio,
                                    Qt.SmoothTransformation)

            self._ui.lastImagePreviewLabel.setPixmap(QPixmap.fromImage(scaled_image))

            # Display captured image for 4 seconds.
            self.displayCapturedImage()
            
            QTimer.singleShot(4000, self.displayViewfinder)

    @Slot()
    def configureCaptureSettings(self):
        if self.m_doImageCapture:
            self.configureImageSettings()
        else:
            self.configureVideoSettings()

    @Slot()
    def configureVideoSettings(self):
        settings_dialog = VideoSettings(self.m_mediaRecorder)

        if settings_dialog.exec():
            settings_dialog.apply_settings()

    @Slot()
    def configureImageSettings(self):
        settings_dialog = ImageSettings(self.m_imageCapture)

        if settings_dialog.exec():
            settings_dialog.apply_image_settings()

    @Slot()
    def record(self):
        self.m_mediaRecorder.record()
        self.updateRecordTime()

    @Slot()
    def pause(self):
        self.m_mediaRecorder.pause()

    @Slot()
    def stop(self):
        self.m_mediaRecorder.stop()

    @Slot(bool)
    def setMuted(self, muted):
        self.m_captureSession.audioInput().setMuted(muted)

    @Slot()
    def takeImage(self):
        self.m_isCapturingImage = True
        print(os.path.join(os.path.dirname(__file__), "images"))
        self.m_imageCapture.captureToFile(os.path.join(os.path.dirname(__file__), "images"))
        if (self.calibration and self.countCalibrate < self.numPhotosCalibrate):
            # Define the time to sleep before taking the next picture
            self.countCalibrate +=1
        elif (self.calibrate ):
            self.timer.stop()
            self.m_isCapturingImage = False
            self.countCalibrate = 0
            self.displayViewfinder()

    @Slot(int, QImageCapture.Error, str)
    def displayCaptureError(self, id, error, errorString):
        #QMessageBox.warning(self, "Image Capture Error", errorString)
        self.m_isCapturingImage = False

    @Slot()
    def startCamera(self):
        self.m_camera.start()

    @Slot()
    def stopCamera(self):
        self.m_camera.stop()

    @Slot()
    def updateCaptureMode(self):
        tab_index = self._ui.captureWidget.currentIndex()
        self.m_doImageCapture = (tab_index == 0)

    @Slot(bool)
    def updateCameraActive(self, active):
        if active:
            self._ui.actionStartCamera.setEnabled(False)
            self._ui.actionStopCamera.setEnabled(True)
            self._ui.captureWidget.setEnabled(True)
            self._ui.actionSettings.setEnabled(True)
        else:
            self._ui.actionStartCamera.setEnabled(True)
            self._ui.actionStopCamera.setEnabled(False)
            self._ui.captureWidget.setEnabled(False)
            self._ui.actionSettings.setEnabled(False)

    @Slot(int)
    def setExposureCompensation(self, index):
        self.m_camera.setExposureCompensation(index * 0.5)

    @Slot()
    def displayRecorderError(self):
        if self.m_mediaRecorder.error() != QMediaRecorder.NoError:
            QMessageBox.warning(self, "Capture Error",
                                self.m_mediaRecorder.errorString())

    @Slot()
    def displayCameraError(self):
        if self.m_camera.error() != QCamera.NoError:
            QMessageBox.warning(self, "Camera Error",
                                self.m_camera.errorString())

    @Slot(QAction)
    def updateCameraDevice(self, action):
        cameras = QMediaDevices.videoInputs()
        for cameraDevice in cameras:
            if cameraDevice.description() == action.iconText():
                self.setCamera(QCameraDevice(cameraDevice))

    @Slot()
    def displayViewfinder(self):
        self._ui.stackedWidget.setCurrentIndex(0)

    @Slot()
    def displayCapturedImage(self):
        self._ui.stackedWidget.setCurrentIndex(1)

    @Slot(bool)
    def readyForCapture(self, ready):
        self._ui.takeImageButton.setEnabled(ready)

    @Slot(int, str)
    def imageSaved(self, id, fileName):
        f = QDir.toNativeSeparators(fileName)
        self._ui.statusbar.showMessage(f"Captured \"{f}\"")

        self.m_isCapturingImage = False
        if self.m_applicationExiting:
            self.close()

    def closeEvent(self, event):
        if self.m_isCapturingImage:
            self.setEnabled(False)
            self.m_applicationExiting = True
            event.ignore()
        else:
            event.accept()

    @Slot()
    def updateCameras(self):
        self._ui.menuDevices.clear()
        available_cameras = QMediaDevices.videoInputs()
        for cameraDevice in available_cameras:
            video_device_action = QAction(cameraDevice.description(),
                                          self._video_devices_group)
            video_device_action.setCheckable(True)
            video_device_action.setData(cameraDevice)
            if cameraDevice == QMediaDevices.defaultVideoInput():
                video_device_action.setChecked(True)

            self._ui.menuDevices.addAction(video_device_action)

    @Slot()
    def showMetaDataDialog(self):
        if not self.m_metaDataDialog:
            self.m_metaDataDialog = MetaDataDialog(self)
        self.m_metaDataDialog.setAttribute(Qt.WA_DeleteOnClose, False)
        if self.m_metaDataDialog.exec() == QDialog.Accepted:
            self.saveMetaData()

    @Slot()
    def saveMetaData(self):
        data = QMediaMetaData()
        for i in range(0, QMediaMetaData.NumMetaData):
            val = self.m_metaDataDialog.m_metaDataFields[i].text()
            if val:
                key = QMediaMetaData.Key(i)
                if key == QMediaMetaData.CoverArtImage:
                    cover_art = QImage(val)
                    data.insert(key, cover_art)
                elif key == QMediaMetaData.ThumbnailImage:
                    thumbnail = QImage(val)
                    data.insert(key, thumbnail)
                elif key == QMediaMetaData.Date:
                    date = QDateTime.fromString(val)
                    data.insert(key, date)
                else:
                    data.insert(key, val)

        self.m_mediaRecorder.setMetaData(data)

    @Slot()
    def startGameOne(self):
        self.readyForCapture(False)

    @Slot()
    def startGameTwo(self):
        self.readyForCapture(False)

    @Slot()
    def displayTracking(self):
        self.readyForCapture(False)

    @Slot()
    def displayStats(self):
        self.readyForCapture(False)
