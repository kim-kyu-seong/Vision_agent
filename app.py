import sys
import winsound

from PyQt6.QtWidgets import (QMainWindow, QApplication, QPushButton, QLabel)


class BeepSound(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("삑 소리 내기")
        self.setGeometry(200, 200, 500, 100)

        short_beep_btn = QPushButton("짧게 삑", self)
        long_beep_btn = QPushButton("길게 삑", self)
        quit_btn = QPushButton("나가기", self)
        self.label = QLabel("환영합니다!", self)

        short_beep_btn.setGeometry(10, 10, 100, 30)
        long_beep_btn.setGeometry(110, 10, 100, 30)
        quit_btn.setGeometry(210, 10, 100, 30)
        self.label.setGeometry(10, 40, 500, 70)

        short_beep_btn.clicked.connect(self.short_beep)
        long_beep_btn.clicked.connect(self.long_beep)
        quit_btn.clicked.connect(self.quit_fn)

# 콜백함수에 다양한 기능을 구현하기 (과제)
    def short_beep(self):
        self.label.setText("주파수 1000으로 0.5초 동안 삑 소리를 냅니다.")
        winsound.Beep(1000, 500)

    def long_beep(self):
        self.label.setText("주파수 1000으로 3초 동안 삑 소리를 냅니다.")
        winsound.Beep(1000, 3000)

    def quit_fn(self):
        self.close()

    

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = BeepSound()
    win.show()
    app.exec()