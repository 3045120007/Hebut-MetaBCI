# -*- coding: utf-8 -*-
#! /usr/bin/env python3

#Author:    FANG Junying  junyinghouse@gmail.com
#Date:      2018/11/13

# Form implementation generated from reading ui file 'emotion.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
import json

class Ui_Processor(object):
    def setupUi(self, ProcessorUI):
        ProcessorUI.setObjectName("ProcessorUI")
        ProcessorUI.resize(400, 400)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("./neuracle_logo_icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        ProcessorUI.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(ProcessorUI)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.gb_device = QtWidgets.QGroupBox(self.centralwidget)
        self.gb_device.setObjectName("gb_device")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.gb_device)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout_3 = QtWidgets.QGridLayout()
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.label_3 = QtWidgets.QLabel(self.gb_device)
        self.label_3.setObjectName("label_3")
        self.gridLayout_3.addWidget(self.label_3, 0, 1, 1, 1)
        self.editSrate = QtWidgets.QLineEdit(self.gb_device)
        self.editSrate.setObjectName("editSrate")
        self.gridLayout_3.addWidget(self.editSrate, 1, 1, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.gb_device)
        self.label_4.setObjectName("label_4")
        self.gridLayout_3.addWidget(self.label_4, 0, 2, 1, 1)
        self.editThreshold = QtWidgets.QLineEdit(self.gb_device)
        self.editThreshold.setObjectName("editThreshold")
        self.gridLayout_3.addWidget(self.editThreshold, 1, 2, 1, 1)
        self.popDevice = QtWidgets.QComboBox(self.gb_device)
        self.popDevice.setObjectName("popDevice")
        self.popDevice.addItem("")
        self.popDevice.addItem("")
        self.gridLayout_3.addWidget(self.popDevice, 1, 0, 1, 1)
        self.label = QtWidgets.QLabel(self.gb_device)
        self.label.setObjectName("label")
        self.gridLayout_3.addWidget(self.label, 0, 0, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout_3)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.gridLayout.addWidget(self.gb_device, 0, 0, 1, 1)
        self.gb_connection = QtWidgets.QGroupBox(self.centralwidget)
        self.gb_connection.setObjectName("gb_connection")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.gb_connection)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout()
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.gridLayout_6 = QtWidgets.QGridLayout()
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.pbOutput = QtWidgets.QPushButton(self.gb_connection)
        self.pbOutput.setObjectName("pbOutput")
        self.gridLayout_6.addWidget(self.pbOutput, 1, 3, 1, 1)
        self.cbDataServer = QtWidgets.QCheckBox(self.gb_connection)
        self.cbDataServer.setObjectName("cbDataServer")
        self.gridLayout_6.addWidget(self.cbDataServer, 0, 0, 1, 1)
        self.cbOutput = QtWidgets.QCheckBox(self.gb_connection)
        self.cbOutput.setObjectName("cbOutput")
        self.gridLayout_6.addWidget(self.cbOutput, 1, 0, 1, 1)
        self.pbDataServer = QtWidgets.QPushButton(self.gb_connection)
        self.pbDataServer.setObjectName("pbDataServer")
        self.gridLayout_6.addWidget(self.pbDataServer, 0, 3, 1, 1)
        self.editPortDataServer = QtWidgets.QLineEdit(self.gb_connection)
        self.editPortDataServer.setText("")
        self.editPortDataServer.setObjectName("editPortDataServer")
        self.gridLayout_6.addWidget(self.editPortDataServer, 0, 2, 1, 1)
        self.editPortOutput = QtWidgets.QLineEdit(self.gb_connection)
        self.editPortOutput.setText("")
        self.editPortOutput.setObjectName("editPortOutput")
        self.gridLayout_6.addWidget(self.editPortOutput, 1, 2, 1, 1)
        self.editIPOutput = QtWidgets.QLineEdit(self.gb_connection)
        self.editIPOutput.setText("")
        self.editIPOutput.setObjectName("editIPOutput")
        self.gridLayout_6.addWidget(self.editIPOutput, 1, 1, 1, 1)
        self.editIPDataServer = QtWidgets.QLineEdit(self.gb_connection)
        self.editIPDataServer.setText("")
        self.editIPDataServer.setObjectName("editIPDataServer")
        self.gridLayout_6.addWidget(self.editIPDataServer, 0, 1, 1, 1)
        self.verticalLayout_6.addLayout(self.gridLayout_6)
        self.horizontalLayout_4.addLayout(self.verticalLayout_6)
        self.gridLayout.addWidget(self.gb_connection, 1, 0, 1, 1)
        self.gb_operation = QtWidgets.QGroupBox(self.centralwidget)
        self.gb_operation.setObjectName("gb_operation")
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout(self.gb_operation)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.verticalLayout_13 = QtWidgets.QVBoxLayout()
        self.verticalLayout_13.setObjectName("verticalLayout_13")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.pbSetParams = QtWidgets.QPushButton(self.gb_operation)
        self.pbSetParams.setObjectName("pbSetParams")
        self.horizontalLayout_5.addWidget(self.pbSetParams)
        self.pbStart = QtWidgets.QPushButton(self.gb_operation)
        self.pbStart.setObjectName("pbStart")
        self.horizontalLayout_5.addWidget(self.pbStart)
        self.verticalLayout_13.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_7.addLayout(self.verticalLayout_13)
        self.gridLayout.addWidget(self.gb_operation, 2, 0, 1, 1)
        ProcessorUI.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(ProcessorUI)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 296, 23))
        self.menubar.setObjectName("menubar")
        ProcessorUI.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(ProcessorUI)
        self.statusbar.setObjectName("statusbar")
        ProcessorUI.setStatusBar(self.statusbar)
        self.retranslateUi(ProcessorUI)
        QtCore.QMetaObject.connectSlotsByName(ProcessorUI)

    def retranslateUi(self, ProcessorUI):
        _translate = QtCore.QCoreApplication.translate
        ProcessorUI.setWindowTitle(_translate("ProcessorUI", "OnlineProcessor"))
        self.gb_device.setTitle(_translate("ProcessorUI", "Device"))
        self.label_3.setText(_translate("ProcessorUI", "SampleRate"))
        self.label_4.setText(_translate("ProcessorUI", "Threshold"))
        self.editSrate.setText(_translate("ProcessorUI", "1000"))
        self.editThreshold.setText(_translate("ProcessorUI", "0.35"))
        self.popDevice.setItemText(0, _translate("ProcessorUI", "Neuracle-64"))
        self.popDevice.setItemText(1, _translate("ProcessorUI", "DSI-24"))
        self.label.setText(_translate("ProcessorUI", "Model"))
        self.cbDataServer.setChecked(True)
        self.cbOutput.setChecked(True)
        self.editIPDataServer.setText('127.0.0.1')
        self.editPortDataServer.setText('8712')
        self.editIPOutput.setText('192.168.1.255')
        self.editPortOutput.setText('6200')
        self.gb_connection.setTitle(_translate("ProcessorUI", "Connection"))
        self.pbOutput.setText(_translate("ProcessorUI", "Connect"))
        self.cbDataServer.setText(_translate("ProcessorUI", "DataServer"))
        self.cbOutput.setText(_translate("ProcessorUI", "Output"))
        self.pbDataServer.setText(_translate("ProcessorUI", "Connect"))
        self.gb_operation.setTitle(_translate("ProcessorUI", "Operation"))
        self.pbSetParams.setText(_translate("ProcessorUI", "SetParameters"))
        self.pbStart.setText(_translate("ProcessorUI", "Start"))

    def update_device_ssvepParas_panel(self):
        idx = self.popDevice.currentIndex()
        self.par['device'] = idx
        self.par['deviceName'] = self.popDevice.currentText()
        device_info = self.device_config[self.par['deviceName']]
        self.par['sampleRate'] = device_info[0]['sampling_rate']
        if idx == 0:
            self.par['nChan'] = 3
            self.editPortDataServer.setText('8712')
        else:
            self.par['nChan'] = len(device_info[0]['montage'][0])
            self.editPortDataServer.setText('8844')
        self.editSrate.setText(str(device_info[0]['sampling_rate']))

    def editThreshold_callback(self):
        self.par['threshold'] = float(self.editThreshold.text())

    def editIPDataServer_callback(self):
        self.par['ipData'] = self.editIPDataServer.text()

    def editPortDataServer_callback(self):
        self.par['portData'] = int(self.editPortDataServer.text())

    def editIPOutput_callback(self):
        self.par['ipOutput'] = self.editIPOutput.text()

    def editPortOutput_callback(self):
        self.par['portOutput'] = int(self.editPortOutput.text())

    def editOperation_callback(self):
        self.par['operation'] = self.editOperation.text()

    def setup_parameters(self):
        self.par = dict()
        device_file = open('./config/device_config.json', 'r')
        self.device_config = json.load(device_file)
        main_file = open('config/main_config.json', 'r')
        main_config = json.load(main_file)
        self.par['buffersize'] = main_config['buffersize']
        self.par['baselinesize'] = main_config['baselinesize']
        self.par['nChan'] = 3
        self.par['ovlap'] = 1
        self.par['isOnline'] = 1
        self.par['isOutput'] = 1
        self.par['nDevice'] = 1
        self.par['deviceName'] = 'Neuracle-64'
        self.par['sampleRate'] = 1000
        self.par['ipData'] = '127.0.0.1'
        self.par['portData'] = 8712
        self.par['ipOutput'] = '127.0.0.1'
        self.par['portOutput'] = 8713


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ui = Ui_Processor()
    W = QtWidgets.QMainWindow()
    ui.setupUi(W)
    W.show()
    sys.exit(app.exec_())
