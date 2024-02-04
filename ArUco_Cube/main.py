# Copyright (C) 2023 The Qt Company Ltd.
# SPDX-License-Identifier: LicenseRef-Qt-Commercial OR BSD-3-Clause

"""PySide6 port of the QtMultiMedia camera example from Qt v6.x"""

import sys

from PySide6 import QtWidgets

from camera import Camera
from pathlib import Path
import cv2


if __name__ == "__main__":
    if not QtWidgets.QApplication.instance():
        app = QtWidgets.QApplication(sys.argv)
    else:
        app = QtWidgets.QApplication.instance()
    camera = Camera()
    camera.show()
    sys.exit(app.exec())