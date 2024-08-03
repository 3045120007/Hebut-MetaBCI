import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QTextEdit, QCheckBox, QPushButton, QHBoxLayout, \
    QLineEdit, QMessageBox
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
class StartScreen(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        # 设置窗口标题和大小
        self.setWindowTitle('开始界面')
        self.setWindowIcon(QIcon('douya.png'))
        #位置位置！！！
        self.setGeometry(590, 250,650, 600)

        # 创建控件
        software_name_label = QLabel('实时脑电的注意力监测系统', self)
        software_name_label.setStyleSheet('font-size: 24px; font-weight: bold;')  # 调整字体大小和加粗

        developer_label = QLabel('开发者：HeBut', self)
        developer_label.setStyleSheet('font-size: 18px;')
        # 设置文本居中
        software_name_label.setAlignment(Qt.AlignCenter)
        # 设置文本右对齐
        developer_label.setAlignment(Qt.AlignRight)
        note_label = QLabel('注意事项：', self)
        note_text = QTextEdit(self)
        note_text.setPlainText('对于医生:\n1.实验开始之前，向患者详细解释实验的目的、过程和预期结果。确保患者清楚地了解实验的目标。\n2.提供明确的仪器操作指导，包括如何正确佩戴脑电设备、如何保持稳定和舒适等。'
                               '3.确保实验环境的安全性，包括正确使用和维护设备、避免电击风险和保持实验室的清洁和整洁。\n4.密切监测患者的状况，包括生理指标、情绪变化和任何不适症状。\n对于被试\n1.遵循医生或技术人员的指示，正确佩戴脑电设备并保持稳定。如果你感到不适或有任何问题，请立即告知医生或技术人员。'
                               '\n2.积极配合医生或技术人员的工作，包括提供准确的个人信息、遵循实验流程和协助记录相关数据。\n3.遵守医生或技术人员的建议和要求，包括关于饮食、药物或其他限制的指示。\n4.对实验过程、结果或后续咨询有任何疑问或需要，及时向医生或技术人员寻求帮助。')
        note_text.setReadOnly(True)  # 设置为只读
        note_text.setStyleSheet("""
            font-size: 18px;
            padding: 8px;
            border: 1px solid #d1d1d1;
            border-radius: 5px;
        """)

        # 创建复选框
        agree_checkbox = QCheckBox('我同意以上注意事项', self)
        note_labell = QLabel('点击方框确认同意后方可进入软件', self)
        note_labell.setAlignment(Qt.AlignCenter)
        agree_checkbox.stateChanged.connect(self.onCheckboxStateChanged)
        image_label = QLabel(self)
        pixmap = QPixmap('path/to/your/image.jpg')  # 请替换为实际图片路径
        image_label.setPixmap(pixmap)
        image_label.setAlignment(Qt.AlignCenter)
        # 创建确认按钮作为实例变量
        self.next_button = QPushButton('确定', self)
        self.next_button.setEnabled(False)
        self.next_button.setStyleSheet("""
                  font-size: 18px;
                  padding: 10px;
                  background-color: #0056b3;
                  color: white;
                  border: none;
                  border-radius: 5px;
              """)
        # 连接按钮的clicked信号到槽函数
        self.next_button.clicked.connect(self.onNextButtonClick)

        # 布局管理
        vbox = QVBoxLayout()
        vbox.addWidget(software_name_label)
        vbox.addWidget(developer_label)
        vbox.addWidget(note_label)
        vbox.addWidget(note_text)
        vbox.addWidget(agree_checkbox)
        vbox.addWidget(image_label)
        vbox.addWidget(self.next_button)
        vbox.addWidget(note_labell)

        btn_close_tasks = QPushButton('终止测试', self)
        btn_close_tasks.clicked.connect(
            self.closeAllTasks)  # Connect button click event to the closeAllTasks slot function
        btn_close_tasks.setFixedSize(100, 25)
        vbox.addWidget(btn_close_tasks, alignment=Qt.AlignRight)


        hbox = QHBoxLayout()
        hbox.addLayout(vbox)

        # 信号与槽连接
        agree_checkbox.stateChanged.connect(lambda state: self.next_button.setEnabled(state == Qt.Checked))

        self.setLayout(hbox)

        self.show()
    def onNextButtonClick(self):
    # 在这里可以执行一些操作，然后关闭窗口
        self.close()

    def closeAllTasks(self):
        sys.exit()
    def onCheckboxStateChanged(self, state):
        # 根据复选框的状态更新按钮的可用性和样式
        self.next_button.setEnabled(state == Qt.Checked)

        if state == Qt.Checked:
            self.next_button.setStyleSheet("""
                QPushButton {
                    font-size: 18px;
                    padding: 10px;
                    background-color: #4CAF50; /* 打钩后的绿色 */
                    color: white;
                    border: none;
                    border-radius: 5px;
                }
            """)
        else:
            self.next_button.setStyleSheet("""
                QPushButton {
                    font-size: 18px;
                    padding: 10px;
                    background-color: #0056b3; /* 初始蓝色 */
                    color: white;
                    border: none;
                    border-radius: 5px;
                }
            """)
            ##007AFF;为亮蓝色


def start_ti():
    app = QApplication(sys.argv)
    start_screen = StartScreen()
    start_screen.show()
    app.exec_()

if __name__ == '__main__':
    start_ti()
