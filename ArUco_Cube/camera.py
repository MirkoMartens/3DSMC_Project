# Copyright (C) 2023 The Qt Company Ltd.
# SPDX-License-Identifier: LicenseRef-Qt-Commercial OR BSD-3-Clause

import os
from pathlib import Path
import time
import random

from PySide6.QtMultimedia import (QAudioInput, QCamera, QCameraDevice,
                                  QImageCapture, QMediaCaptureSession,
                                  QMediaDevices, QMediaMetaData,
                                  QMediaRecorder, QVideoFrame, QVideoSink, QMediaPlayer)
from PySide6.QtWidgets import QDialog, QMainWindow, QMessageBox, QApplication as qApp
from PySide6.QtGui import QAction, QActionGroup, QIcon, QImage, QPixmap, QPainter, QFont, QColor, QPen, QFontMetrics,QCursor
from PySide6.QtCore import QDateTime, QDir, QTimer, Qt, Slot, qWarning,QRect,QSize
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
import Questions


from calibration import start_calibration
from QeA import SaverReader

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
        self.timerCount = False
        self.timerQuest = None
        self.timerQuestGuest = None
        self.waitMax = 1
        self.number = self.waitMax
        self.delayQuestion = 10
        self.showQuestion = False
        self.endQuestion = False
        self.showResult = False
        self.endGame = False
        self.color = "white"
        self.showAnswer = False
        self.position = -1
        self.delayAnswer = 5
        self.id = 0
        self.answerFound = ""
        self.timerAnswer = None
        self.countQuestion = 0
        self.maxQuestion = 10
        self.user_score = 0
        self.numberGuess = self.delayAnswer
        self._ui.setupUi(self)
        image = os.path.join(Path(__file__).parent, "shutter.svg")
        self._ui.takeImageButton.setIcon(QIcon(os.fspath(image)))
        self._ui.actionAbout_Qt.triggered.connect(qApp.aboutQt)
        
        # Create variables for questions
        self.filePath = os.path.join(Path(__file__).parent, "Questions.json")
        self.questions = Questions.Questions(self.filePath)
        self.question = None
        self.text =""
        self.textTimer = ""
        self.answer_1 = ""
        self.answer_2 = ""
        self.answer_3 = ""
        self.right_answer = ""
        self.wrong_answer1 = ""
        self.wrong_answer2 = ""

        # create variables to store calibration variables
        self.ret = None
        self.camera_matrix = None
        self.distortion_coefficients = None
        self.rotation_vectors = None
        self.translation_vectors = None

        # create variables for games
        self.isStartGameOne = False

        # create variables for CheckBox
        self.isTracking = False
        self.isDisplayTracking = False
        self.isDisplayStats = False

        # create variables for ArUco
        self.arucoDict = cv2.aruco.DICT_4X4_50
        self.aruco_dict =  cv2.aruco.getPredefinedDictionary(self.arucoDict)
        self.corners = None
        self.ids = None
        self.rejected = None
        self.result = None

        # create variables for json dump
        self.saver_reader = SaverReader("json_dump.json")

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
            self.m_imageCapture.imageCaptured.connect(self.drawArucoMarkers)
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
        self.delayPhotos = 3000
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
            self.timerQuest = time.time()
            self.timerCount = True
            self.timerLoop.start(20) 
            
        self.m_imageCapture.capture() 
            
    @Slot()
    def drawArucoMarkers(self, requestId, image):
        if self.isTracking:
            image = scaled_image = image.scaledToWidth(self._ui.viewfinder.size().width()*0.998,  Qt.SmoothTransformation)
            # Convert QImage to NumPy array
            image_array = np.array(scaled_image.constBits()).reshape(scaled_image.height(), scaled_image.width(), 4).copy()  # Assuming the image is RGBA
            # Convert RGBA to BGR (OpenCV uses BGR)
            opencv_image = cv2.cvtColor(image_array, cv2.COLOR_RGBA2RGB)

            # Detect Aruco markers
            self.corners, self.ids, self.rejected = cv2.aruco.detectMarkers(opencv_image, self.aruco_dict)

            # Draw detected markers
            if self.isDisplayTracking:
                # Ensure self.result is initialized as a NumPy array
                self.result = opencv_image.copy()

                # Show image with detected markers
                cv2.aruco.drawDetectedMarkers(self.result, self.corners, self.ids)

                # Convert the modified image to QImage for display
                height, width, channel = self.result.shape
                bytes_per_line = 3 * width
                image = QImage(self.result.data, width, height, bytes_per_line, QImage.Format_RGB888)

                # Display the image
                self._ui.lastImagePreviewLabel.setPixmap(QPixmap.fromImage(image))
                self.displayCapturedImage()
            else:
                self.displayViewfinder()


    @Slot()
    def imageCapturedText(self, request_id, image):
        # Slot to handle captured images
        # Add text to the image
        self.question = self.questions.get_question()
        if (not self.endGame):
            if (self.loop and self.isStartGameOne):
                self.isTracking = False
                #scaled_image = image.scaled(self._ui.viewfinder.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
                scaled_image = image.scaledToWidth(self._ui.viewfinder.size().width() * 0.998,  Qt.SmoothTransformation)
                if self.timerCount and not self.endQuestion :
                    if time.time() - self.timerQuest > 1:
                        self.number -=1
                        self.timerQuest = time.time()
                    self.text = str(self.number)
                else:
                    if time.time() - self.timerQuestGuest > 1:
                        self.numberGuess -=1
                        self.timerQuestGuest = time.time()
                    self.textTimer = str(self.numberGuess)
                if self.number < 0 and not self.showQuestion and not self.endQuestion:
                    self.timerCount = False
                    self.showQuestion = True

                    self.text = self.question['question']
                    self.answer_1 = self.question['answers'][0]
                    self.answer_2 = self.question['answers'][1]
                    self.answer_3 = self.question['answers'][2]
                    self.right_answer = self.answer_1
                    self.timerQuest = time.time()
                    self.timerAnswer = time.time()
                    self.timerQuestGuest = time.time()
                    self.countQuestion +=1
                    self.showAnswer = False
                if self.showQuestion:
                    if time.time() - self.timerQuest > self.delayQuestion:
                        self.text = self.question['question']
                        self.right_answer = self.question['answers'][0]
                        self.wrong_answer1 = self.question['answers'][1]
                        self.wrong_answer2 = self.question['answers'][2]
                        random.shuffle(self.question["answers"])
                        self.answer_1 = self.question['answers'][0]
                        self.answer_2 = self.question['answers'][1]
                        self.answer_3 = self.question['answers'][2]
                        self.timerQuest = time.time()
                        self.timerAnswer = time.time()
                        self.timerQuestGuest = time.time()
                        self.showAnswer = False
                        self.number = -1
                        self.countQuestion += 1
                        self.position = -1
                        self.answerId = -1
                        self.answerFound = ""
                        self.textTimer = ""
                        self.numberGuess = self.delayAnswer
                    if time.time() - self.timerAnswer > self.delayAnswer:
                        # Get the current position of the mouse
                        if (self.position == -1):
                            # this just gets called once as soon as the question time is over
                            self.position = QCursor.pos().x()
                            if (self.position < self._ui.viewfinder.size().width()/3):
                                self.answerFound = self.answer_1
                            elif (self.position < 2*self._ui.viewfinder.size().width()/3):
                                self.answerFound = self.answer_2
                            else:   
                                self.answerFound = self.answer_3

                            if self.answerFound == self.right_answer:
                                self.user_score += 100
                            
                            # dumping the question, user answer and correct/wrong answer choices to a json
                            self.saver_reader.save_question(self.question['question'], self.answerFound, self.right_answer, self.wrong_answer1, self.wrong_answer2)
                        self.showAnswer = True

                image_with_text = self.addTextToImage(scaled_image, self.text, (Qt.AlignTop| Qt.AlignHCenter))
                image_with_text = self.addTextToImage(image_with_text,str(self.user_score), (Qt.AlignTop| Qt.AlignRight))
                if self.showQuestion:
                    self.id = 1
                    image_with_text = self.addTextToImage(image_with_text, self.answer_1,  Qt.AlignVCenter | Qt.AlignLeft, self.color)
                    self.id = 2
                    image_with_text = self.addTextToImage(image_with_text, self.answer_2, Qt.AlignVCenter | Qt.AlignHCenter,self.color)
                    self.id = 3
                    image_with_text = self.addTextToImage(image_with_text, self.answer_3, Qt.AlignVCenter | Qt.AlignRight,self.color)
                    self.id = 0
                    if (self.numberGuess <= 0):
                        self.numberGuess = self.delayQuestion - self.delayAnswer
                        self.textTimer = str(self.numberGuess)
                    image_with_text = self.addTextToImage(image_with_text, self.textTimer, Qt.AlignTop | Qt.AlignLeft,self.color)
                if self.countQuestion > self.maxQuestion:
                    self.saver_reader.finish_json() # necessary to make the json file correct                
                    self.countQuestion = 0
                    self.showQuestion = False
                    self.endQuestion = True
                    self.timerCount = False
                    self.isStartGameOne = False
                    self._ui.trackingCheckBox.setEnabled(True)
                    self._ui.statsCheckBox.setEnabled(True)
                    self.text = "End of Question"
                    self.endGame = True 
                    self.timerCount = -1
                else:
                    # Display the modified image
                    self._ui.lastImagePreviewLabel.setPixmap(QPixmap.fromImage(image_with_text))

                    # Display captured image for 4 seconds.
                    self.displayCapturedImage()
        else:
            self.text = "Make a winner pose"
            scaled_image = image.scaledToWidth(self._ui.viewfinder.size().width() * 0.998,  Qt.SmoothTransformation)
            image_with_text = self.addTextToImage(scaled_image, self.text, Qt.AlignVCenter | Qt.AlignHCenter,self.color)
            if (self.timerCount < 0):
                self.timerQuest = time.time()
                self.timerCount = 5
            if time.time() - self.timerQuest > 1:
                self.timerQuest = time.time()
                self.timerCount -= 1 
            if (self.timerCount == 0):
                self.timerLoop.stop()
                text = " Your wonderful shitty score is " + str(self.user_score)
                image_with_text = self.addTextToImage(scaled_image, text, Qt.AlignTop | Qt.AlignHCenter,self.color)
            else:
                image_with_text = self.addTextToImage(image_with_text, str(self.timerCount), Qt.AlignTop | Qt.AlignHCenter,self.color)
            self._ui.lastImagePreviewLabel.setPixmap(QPixmap.fromImage(image_with_text))


        
    @Slot()
    def addTextToImage(self, image, text, position, color = "white"):
        # Create a QPixmap from the QImage
        pixmap = QPixmap.fromImage(image)

        # Create a QPainter to draw on the image
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)

        # Set font and color for the overlay text
        font = QFont("Arial", 16)
        color = QColor("black")
        painter.setFont(font)
        width,height = pixmap.width(), pixmap.height()
        if self.id > 0:
            rectangle = painter.drawText(pixmap.rect(),position, text)
            painter.setPen("black")
            if self.showAnswer:
                if self.id == 1 and self.right_answer == self.answer_1:
                    color = QColor("green")
                elif self.id == 2 and self.right_answer == self.answer_2:
                    color = QColor("green")
                elif self.id == 3 and self.right_answer == self.answer_3:
                   color = QColor("green")
                else:
                    color = QColor("red")
                if (self.right_answer == self.answerFound):
                    painter.drawText(width/2,height/3, "Correct")
                else:
                    painter.drawText(width/2,height/3, "Wrong")
            else:
                color = QColor("black")

            painter.setPen(color)
            
            painter.drawRect(rectangle)

        # Draw the overlay text at the bottom of the image
        else:
            painter.setPen(color)
            painter.drawText(pixmap.rect(),position, text)
            painter.drawLine(0,height *0.1,width,height *0.1)
            painter.drawLine(width/3,height *0.1,width/3,height)
            painter.drawLine(2*width/3,height *0.1,2*width/3,height)

        # End painting
        painter.end()

        # Convert the QPixmap back to a QImage
        modified_image = pixmap.toImage()

        return modified_image


    @Slot()
    def takeCalibrationImages(self):
        self.calibration = True
        self.timer = QTimer(self.m_camera)
        self.timer.timeout.connect(self.takeCalibrationImage)
        # Define the time to take x photos in miliseconds
        self.timer.start(self.delayPhotos)

    def calibrate(self):
        self.ret, self.camera_matrix, self.distortion_coefficients0, self.rotation_vectors, self.translation_vectors = start_calibration(os.path.join(os.path.dirname(__file__), "images", "calibration"))
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
        self.m_imageCapture.captureToFile(os.path.join(os.path.dirname(__file__), "images"))

    def takeCalibrationImage(self):
        self.m_isCapturingImage = True
        print(os.path.join(os.path.dirname(__file__), "images", "calibration"))
        self.m_imageCapture.captureToFile(os.path.join(os.path.dirname(__file__), "images", "calibration"))
        if (self.calibration and self.countCalibrate < self.numPhotosCalibrate):
            # Define the time to sleep before taking the next picture
            self.countCalibrate +=1
        elif (self.takeCalibrationImages):
            self.timer.stop()
            self.m_isCapturingImage = False
            self.countCalibrate = 0
            self.displayViewfinder()
            self.calibration = False

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
        self.isStartGameOne = True
        self._ui.trackingCheckBox.setEnabled(False)
        self._ui.statsCheckBox.setEnabled(False)
        #self.isTracking = True
        self.captureFrameLoop()

    @Slot()
    def startGameTwo(self):
        self._ui.trackingCheckBox.setEnabled(False)
        self._ui.statsCheckBox.setEnabled(False)
        self.readyForCapture(False)
        
    @Slot()
    def quitGame(self):
        self.loop = False
        self.isStartGameOne = False
        self.timerLoop.stop()
        self.showQuestion = False
        self.number = self.waitMax
        self.timerCount = False
        self.displayViewfinder()
        self.updateCameraActive(self.m_camera.isActive())
        self._ui.trackingCheckBox.setCheckState(Qt.Unchecked)
        self.isDisplayTracking = False
        self._ui.trackingCheckBox.setEnabled(True)
        self._ui.statsCheckBox.setEnabled(True)
        self.displayViewfinder()

    @Slot()
    def displayTracking(self):
        if not self.isDisplayTracking:
            self.isTracking = True
            self.isDisplayTracking = True
            self.captureFrameLoop()
            print("Displaying tracking")
        else:
            self.isDisplayTracking = False
            self.loop = False
            self.timerLoop.stop()
            self.displayViewfinder()
            print("Not displaying tracking")

    @Slot()
    def displayStats(self):
        if not self.isDisplayStats:
            self.isDisplayStats = True
            print("Not displaying stats")
        else:
            self.isDisplayStats = False
            print("Displaying stats")
