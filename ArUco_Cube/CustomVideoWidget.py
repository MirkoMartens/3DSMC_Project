from PySide6.QtWidgets import  QVBoxLayout, QWidget, QApplication
from PySide6.QtGui import QPainter, QColor, QFont
from PySide6.QtMultimediaWidgets import QVideoWidget
from PySide6.QtCore import Qt, QTimer
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QFrame

class CustomVideoWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.overlayText = "Hello, World!"
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateOverlayText)
        self.timer.start(1000) 
        
        
    def updateOverlayText(self):
        # Update overlay text each time the timer triggers
        self.overlayText = "New Text"
        print("Overlay Text:", self.overlayText)
        self.update()

    def setOverlayText(self, text):
        self.overlayText = text
        self.update()

    def paintEvent(self, event):
        # Call the base class paintEvent to render the video content
        super().paintEvent(event)

        # Create a QPainter to draw on top of the video
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        textRect = self.rect()

        # Set font and color for the overlay text
        painter.setFont(QFont("Arial", 16))
        painter.setPen(QColor("white"))

        # Draw the overlay text at the center of the video widget
        print("Overlay Text:", self.overlayText)
        painter.drawText(textRect, Qt.AlignCenter, self.overlayText)