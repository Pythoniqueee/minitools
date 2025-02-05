import sys
import pyautogui
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget

class MousePositionApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("鼠标坐标工具")
        self.setGeometry(100, 100, 250, 100)  # 设置窗口大小和位置

        # 创建 UI
        self.layout = QVBoxLayout()
        self.label = QLabel("鼠标坐标: (X, Y)")
        self.layout.addWidget(self.label)
        self.setLayout(self.layout)

        # 创建定时器，定时更新鼠标位置
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_mouse_position)
        self.timer.start(0)  # 每 100ms 更新一次鼠标坐标

    def update_mouse_position(self):
        """获取并更新鼠标坐标"""
        x, y = pyautogui.position()
        self.label.setText(f"鼠标坐标: (x: {x}, y: {y})")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MousePositionApp()
    window.show()
    sys.exit(app.exec_())

