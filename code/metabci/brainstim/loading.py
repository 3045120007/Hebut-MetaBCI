import sys
from PyQt5.QtWidgets import QApplication, QWidget, QProgressBar, QVBoxLayout, QLabel, QDesktopWidget
from PyQt5.QtCore import QTimer, Qt

class MyWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        # 隐藏标题栏和最小化、最大化、关闭按钮
        self.setWindowFlags(Qt.FramelessWindowHint)

        # 创建进度条
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(100)

        # 设置进度条样式
        self.progress_bar.setStyleSheet("""
            # QProgressBar {
            #     border: 2px solid grey;
            #     border-radius: 5px;
            #     background-color: #FFFFFF;
            # }

            QProgressBar::chunk {
                background-color: #05B8CC;
                width: 5px;
                margin: 0.5px;
            }

            QProgressBar::sub-page {
                background-color: #05B8CC;
            }
        """)

        # 创建标签用于显示文本
        self.label = QLabel('Loading...', self)
        self.label.setAlignment(Qt.AlignCenter)

        # 设置标签样式
        self.label.setStyleSheet("""
            QLabel {
                font-size: 18px;
                color: #05B8CC;
            }
        """)

        # 创建布局并将进度条和标签添加到布局中
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.progress_bar)

        # 设置窗口布局
        self.setLayout(layout)

        # 设置定时器，每隔一段时间更新进度条和标签
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_progress)
        self.timer.start(19.8)  # 定时器间隔设为26毫秒

        # 设置定时器，2.6秒后关闭窗口
        QTimer.singleShot(2000, self.close)

        # 设置窗口属性
        self.setGeometry(760 ,400,300, 150)
        # 获取屏幕的尺寸
        screen_size = QDesktopWidget().screenGeometry()

        # # 计算窗口在屏幕中央的位置
        # x = (screen_size.width() ) // 2
        # y = (screen_size.height() ) // 2
        # 移动窗口到中央
        #self.move(x, y)
        self.show()

    def update_progress(self):
        # 每次定时器触发，增加进度条的值
        current_value = self.progress_bar.value()
        if current_value < 100:
            self.progress_bar.setValue(current_value + 1)

        # 更新标签文本
        self.label.setText(f'<font color="#0056b3" size="5">Loading... {current_value}%</font>')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyWindow()
    sys.exit(app.exec_())
def loading():
    app = QApplication(sys.argv)
    window = MyWindow()
    app.exec_()