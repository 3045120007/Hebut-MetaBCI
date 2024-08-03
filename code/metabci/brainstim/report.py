import sys

from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QPushButton, QHBoxLayout, QMessageBox, \
    QDesktopWidget
from PyQt5.QtCore import Qt

class ReportDialog(QWidget):
    def __init__(self, name, gender, age, custom_info):
        super().__init__()
        self.init_ui(name, gender, age, custom_info)

    def init_ui(self, name, gender, age, custom_info):
        # 创建显示信息的标签
        self.setWindowIcon(QIcon('douya.png'))
        info_label = QLabel(
            f'<b>姓名:</b> {name}<br><b>性别:</b> {gender}<br><b>年龄:</b> {age}<br><b>检测报告:</b> {custom_info}')
        info_label.setAlignment(Qt.AlignCenter)
        global nname
        nname=name
        # 启用自动换行
        info_label.setWordWrap(True)

        # 创建两个按钮
        close_button = QPushButton('退出')
        close_button.clicked.connect(self.close)

        export_button = QPushButton('导出报告')
        export_button.clicked.connect(self.export_report)

        # 设置按钮样式
        button_style = """
            QPushButton {
                font-size: 18px;
                padding: 10px;
                background-color: #007AFF;
                color: white;
                border: none;
                border-radius: 15px; /* 设置大一些的圆角 */
                margin: 0 30px; /* 设置两边的距离 */
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
        """
        close_button.setStyleSheet(button_style)
        export_button.setStyleSheet(button_style)
        image_label = QLabel(self)
        pixmap = QPixmap('result_plot1.png')  # 替换 'your_image.png' 为你的图片路径
        image_label.setPixmap(pixmap)
        image_label.setAlignment(Qt.AlignCenter)
        # 设置布局
        layout = QVBoxLayout()
        layout.addWidget(image_label)
        layout.addWidget(info_label)
        # 创建水平布局并添加按钮
        button_layout = QHBoxLayout()
        button_layout.addWidget(close_button)
        button_layout.addWidget(export_button)
        layout.addLayout(button_layout)

        # 设置窗口属性
        self.setLayout(layout)
        self.setWindowTitle('测试报告')
        self.setGeometry(590, 250, 650, 550)

        # 设置样式
        self.setStyleSheet("""
            QLabel {
                font-size: 18px;
            }
            QLineEdit {
                font-size: 18px;
                padding: 8px;
                border: 1px solid #d1d1d1;
                border-radius: 5px;
            }
        """)

    def export_report(self):
        report_file = str(nname)+'.html'

        # 弹出提示框
        msg_box = QMessageBox()
        msg_box.setStyleSheet("QLabel{"
                             "min-width: 150px;"
                             "min-height: 110px; "
                             "}")
        msg_box.setWindowIcon(QIcon('douya.png'))
        msg_box.setIcon(QMessageBox.Information)
        msg_box.setText(f'报告已成功导出为 {report_file}')
        msg_box.setWindowTitle('导出成功')
        msg_box.setStandardButtons(QMessageBox.Open | QMessageBox.Close)
        # 设置对话框大小
        big_icon = QIcon('group.png')  # 替换为你自己的大图标路径
        msg_box.setIconPixmap(big_icon.pixmap(128, 128))  # 调整大小
        # 设置按钮响应函数
        close_button = msg_box.button(QMessageBox.Close)
        close_button.setText('关闭程序')
        close_button.setStyleSheet("""QPushButton { 
                font-size: 18px;
                padding: 12px; /* 增加内边距 */
                background-color: #007AFF;
                color: white;
                border: none;
                font-weight: bold;
                border-radius: 20px;
                margin: 0 40px; /* 调整外边距 */}
                QPushButton:hover {
                background-color: #0056b3;
                transition: background-color 0.3s; /* 添加过渡效果 */
            }
            """)  # 设置按钮样式
        close_button.clicked.connect(self.close)

        open_button = msg_box.button(QMessageBox.Open)
        open_button.setText('打开报告并关闭程序')  # 修改打开按钮文本
        open_button.setStyleSheet("""QPushButton { 
                font-size: 18px;
                padding: 12px; /* 增加内边距 */
                background-color: #007AFF;
                color: white;
                font-weight: bold;
                border: none;
                border-radius: 20px;
                margin: 0 40px; /* 调整外边距 */}
                QPushButton:hover {
                background-color: #0056b3;
                transition: background-color 0.3s; /* 添加过渡效果 */
            }
            """)  # 设置按钮样式
        open_button.clicked.connect(lambda: self.open_report(report_file))
        open_button.clicked.connect(self.close)
        # 显示提示框
        msg_box.exec_()

    def open_report(self, report_file):
        # 在这里打开报告文件的逻辑，可以使用webbrowser模块
        import webbrowser
        webbrowser.open(report_file)

def report(name, gender, age, custom_info=''):
    # 创建一个应用程序对象
    app = QApplication(sys.argv)

    # 创建报告对话框对象，并传入用户信息以及其他可选信息
    dialog = ReportDialog(name, gender, age, custom_info="目前来看，未在测试者身上检测出注意缺陷多动障碍，被测试者全程注意力集中。")

    # 显示报告对话框
    dialog.show()

    # 运行应用程序，进入事件循环，直到用户关闭对话框
    sys.exit(app.exec_())

# Example Usage
#report("张三", "男", 25, 3, "目前来看，未在测试者身上检测出注意缺陷多动障碍，被测试者全程注意力集中。")
