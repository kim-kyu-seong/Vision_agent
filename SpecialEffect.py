import cv2
import numpy as np
from PyQt6.QtWidgets import (
    QMainWindow, QApplication, QPushButton, QLabel, QFileDialog, QComboBox, QMessageBox
    )

import sys


class SpecialEffect(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("사진 특수 효과")
        self.setGeometry(200, 200, 800, 200)

        pictureButton = QPushButton("사진 읽기", self)
        embossButton = QPushButton("엠보싱", self)
        cartoonButton = QPushButton("카툰", self)
        sketchButton = QPushButton("연필 스케치", self)
        oilButton = QPushButton("유화", self)
        saveButton = QPushButton("저장하기", self)
        self.pickCombo = QComboBox(self)
        self.pickCombo.addItems(["엠보싱", "카툰", "연필 스케치(명암)", "연필 스케치(컬러)", "유화"])
        quitButton = QPushButton("나가기", self)
        self.label = QLabel("환영합니다!", self)

        pictureButton.setGeometry(10, 10, 100, 30)
        embossButton.setGeometry(110, 10, 100, 30)
        cartoonButton.setGeometry(210, 10, 100, 30)
        sketchButton.setGeometry(310, 10, 100, 30)
        oilButton.setGeometry(410, 10, 100, 30)
        saveButton.setGeometry(510, 10, 100, 30)
        self.pickCombo.setGeometry(510, 40, 110, 30)
        quitButton.setGeometry(620, 10, 100, 30)
        self.label.setGeometry(10, 40, 500, 170)

        pictureButton.clicked.connect(self.pictureOpenFunction)
        embossButton.clicked.connect(self.embossFunction)
        cartoonButton.clicked.connect(self.cartoonFunction)
        sketchButton.clicked.connect(self.sketchFunction)
        oilButton.clicked.connect(self.oilFunction)
        saveButton.clicked.connect(self.saveFunction)
        quitButton.clicked.connect(self.quitFunction)

    def pictureOpenFunction(self):
        fname, _ = QFileDialog.getOpenFileName(self, "사진 읽기", "", "Images (*.png *.jpg *.jpeg *)")
        
        if not fname:
            # 사용자가 파일을 선택하지 않았을 경우
            self.label.setText("파일을 선택하지 않았습니다.")
            return
        
        self.img = cv2.imread(fname)
        if self.img is None:
            # 이미지가 None이면 경고 메시지를 표시하고 프로그램을 종료하지 않음
            QMessageBox.critical(self, "오류", "이미지를 불러올 수 없습니다. 지원되지 않는 형식이거나 손상된 파일일 수 있습니다.")
            return

        # 이미지가 정상적으로 불러와졌을 경우
        self.label.setText("이미지를 성공적으로 불러왔습니다!")
        cv2.imshow("Painting", self.img)

    def embossFunction(self):
        femboss = np.array([[-1.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 1.0]])

        gray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
        gray16 = np.int16(gray)
        self.emboss = np.uint8(np.clip(cv2.filter2D(gray16, -1, femboss) + 128, 0, 255))

        cv2.imshow("Emboss", self.emboss)

    def cartoonFunction(self):
        self.cartoon = cv2.stylization(self.img, sigma_s=60, sigma_r=0.45)
        cv2.imshow("Cartoon", self.cartoon)

    def sketchFunction(self):
        self.sketch_gray, self.sketch_color = cv2.pencilSketch(
            self.img, sigma_s=60, sigma_r=0.07, shade_factor=0.02
        )
        cv2.imshow("Pencil sketch(gray)", self.sketch_gray)
        cv2.imshow("Pencil sketch(color)", self.sketch_color)

    def oilFunction(self):
        self.oil = cv2.xphoto.oilPainting(self.img, 10, 1, cv2.COLOR_BGR2Lab)
        cv2.imshow("Oil painting", self.oil)

    def saveFunction(self):
        fname = QFileDialog.getSaveFileName(self, "파일 저장", "./")

        i = self.pickCombo.currentIndex()
        if i == 0:
            cv2.imwrite(fname[0], self.emboss)
        elif i == 1:
            cv2.imwrite(fname[0], self.cartoon)
        elif i == 2:
            cv2.imwrite(fname[0], self.sketch_gray)
        elif i == 3:
            cv2.imwrite(fname[0], self.sketch_color)
        elif i == 4:
            cv2.imwrite(fname[0], self.oil)

    def quitFunction(self):
        cv2.destroyAllWindows()
        self.close()


app = QApplication(sys.argv)
win = SpecialEffect()
win.show()
app.exec()