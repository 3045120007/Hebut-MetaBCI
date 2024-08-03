# 导入必要的库
import sys
import threading

from PyQt5.QtCore import Qt
from PyQt5.QtSerialPort import QSerialPortInfo
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QVBoxLayout, QPushButton, QFormLayout, QComboBox, \
    QStatusBar, QHBoxLayout
from PyQt5.QtGui import QIcon, QPixmap
import serial.tools.list_ports
from validation_test import *
# 创建用户信息对话框的类
class UserInfoDialog(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("基于实时脑电的注意力检测系统")
        self.setWindowIcon(QIcon('douya.png'))
        self.setGeometry(590, 250,650, 550)
        self.init_ui()
        self.name = None
        self.gender = None
        self.age = None
        self.experiment_count = None

    def init_ui(self):
        # 创建标签和文本框用于输入用户信息
        self.name_label = QLabel('测试者姓名:')
        self.name_edit = QLineEdit(self)
        self.name_edit.textChanged.connect(self.on_text_changed)
        self.name_edit.textChanged.connect(self.onn_text_changed)


        self.gender_label = QLabel('测试者性别:')
        self.gender_edit = QLineEdit(self)
        self.gender_edit.textChanged.connect(self.on_gender_changed)

        self.age_label = QLabel('测试者年龄:')
        self.age_edit = QLineEdit(self)
        self.age_edit.textChanged.connect(self.on_age_changed)

        self.experiment_label = QLabel('动画选择（1，2）:')
        self.experiment_edit = QLineEdit(self)
        self.experiment_edit.textChanged.connect(self.on_exp_changed)

        # 创建确认按钮，并连接到槽函数 on_confirm
        self.confirm_button = QPushButton('正式监测')
        self.confirm_button.clicked.connect(self.on_confirm)

        # 创建正式监测按钮，并连接到槽函数 on_monitor
        self.monitor_button = QPushButton('校验')
        self.monitor_button.clicked.connect(self.on_test)
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.monitor_button)
        button_layout.addWidget(self.confirm_button)
        # 使用 QFormLayout 管理表单布局
        form_layout = QFormLayout()
        form_layout.addRow(self.name_label, self.name_edit)
        form_layout.addRow(self.gender_label, self.gender_edit)
        form_layout.addRow(self.age_label, self.age_edit)
        form_layout.addRow(self.experiment_label, self.experiment_edit)
        form_layout.addRow(button_layout)

        # 在最下面添加提示性语句
        self.tip_label = QLabel('请医生协助用户填写完整信息后再点击确认按钮。')
        self.tip_label.setStyleSheet('font-size: 16px;')  # 调整字体大小和加粗
        self.tip_label.setAlignment(Qt.AlignCenter)
        form_layout.addRow(self.tip_label)
        btn_close_tasks = QPushButton('终止测试', self)
        btn_close_tasks.clicked.connect(
            self.closeAllTasks)  # Connect button click event to the closeAllTasks slot function
        btn_close_tasks.setFixedSize(275, 25)
        btn_close_tasks.setStyleSheet("QPushButton {"
                                      
                                      "   background-color: #f6f6f6;"
                                      "padding: 0px"
                                      "   }"
                                      "QPushButton:hover {"
                                      "   background-color: #dcdcdc;"
                                      "}")
        form_layout.addRow("", btn_close_tasks)
        # 在布局的顶部添加 logo
        logo_label = QLabel(self)
        logo_label.setPixmap(QPixmap('mas.png'))  # 替换为你的logo路径
        pixmap = QPixmap('mas.png')
        logo_label.setPixmap(pixmap.scaled(280, 280))
        form_layout.insertRow(0, logo_label)
        logo_label.setAlignment(Qt.AlignCenter)

        # 使用 QHBoxLayout 包装表单布局，并添加左右间距
        main_layout = QHBoxLayout()
        main_layout.addSpacing(50)  # 左侧间距
        main_layout.addLayout(form_layout)
        main_layout.addSpacing(50)  # 右侧间距
        self.confirm_button.setEnabled(False)
        # 将整体布局设置给窗口
        self.setLayout(main_layout)

        # 设置一些基本样式
        self.setStyleSheet("""
            QLabel {
                font-size: 18px;
                padding: 5px;  /* 调整标签的内边距 */
            }

            QLineEdit {
                font-size: 18px;
                padding: 8px;
                border: 2px solid #007AFF;  /* 默认边框颜色 */
                border-radius: 10px;
            }
            QLineEdit:focus {
            border: 2px solid #0056b3;
        }

            QLineEdit:focus {
                border: 2px solid #0056b3;  /* 设置焦点时的边框颜色 */
            }

            QPushButton {
                font-size: 18px;
                padding: 10px;
                background-color: #007AFF;
                color: white;
                border-radius: 10px;  /* 调整边框圆角 */
            }

            QPushButton:hover {
                background-color: #4CAF50;
            }
        """)


    def onn_text_changed(self):
        # 当姓名栏有输入时启用确认按钮
        self.confirm_button.setEnabled(bool(self.name_edit.text()))
        self.monitor_button.setEnabled(bool(self.name_edit.text()))

    def on_test(self):
        self.monitoring_page = create_interface()  # 创建监测页面实例
        # self.monitoring_page.run()  # 显示监测页面

    def on_confirm(self):
        # 从文本框中获取用户输入的姓名、性别、年龄和实验次数，并存储在对应的属性中
        self.name = self.name_edit.text()
        self.gender = self.gender_edit.text()
        self.age = self.age_edit.text()
        self.experiment_count = self.experiment_edit.text()

        # 关闭对话框
        self.close()

    def closeAllTasks(self):
        sys.exit()
    def on_text_changed(self):
        if self.name_edit.text():
            self.name_edit.setStyleSheet("border: 2px solid #4CAF50;")
        else:
            self.name_edit.setStyleSheet("border: 2px solid #007AFF;")
    def on_gender_changed(self):
        if self.gender_edit.text()=='男' or self.gender_edit.text()=='女':
            self.gender_edit.setStyleSheet("border: 2px solid #4CAF50;")
        else:
            self.gender_edit.setStyleSheet("border: 2px solid #007AFF;")
    def on_age_changed(self):
        if self.age_edit.text().isdigit():
            self.age_edit.setStyleSheet("border: 2px solid #4CAF50;")
        else:
            self.age_edit.setStyleSheet("border: 2px solid #007AFF;")
    def on_exp_changed(self):
        if self.experiment_edit.text().isdigit():
            self.experiment_edit.setStyleSheet("border: 2px solid #4CAF50;")
        else:
            self.experiment_edit.setStyleSheet("border: 2px solid #007AFF;")

    # def handle_com_port_selected(self, index):
    #     # 获取当前选择的COM端口
    #     selected_com_port = self.sender().currentText()
    #     print(f"当前选择的COM端口是: {selected_com_port}")
def massage():
    # 创建应用程序对象
    app = QApplication(sys.argv)

    # 创建用户信息输入对话框
    user_info_dialog = UserInfoDialog()

    # 显示用户信息输入对话框
    user_info_dialog.show()

    # 启动应用程序的事件循环
    app.exec_()

    # 从对话框中获取用户输入的信息
    name = user_info_dialog.name
    gender = user_info_dialog.gender
    age = user_info_dialog.age
    experiment_count = user_info_dialog.experiment_count

    # 返回获取到的用户信息
    return name, gender, age, experiment_count
    # return name, gender, age



if __name__ == '__main__':
    massage()
