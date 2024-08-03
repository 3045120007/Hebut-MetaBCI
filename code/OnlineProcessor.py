# -*- coding: utf-8 -*-
# License: MIT License
"""
SSAVEP Feedback on NeuroScan.

"""
import time
import serial
import numpy as np
import sys
from PyQt5 import QtWidgets
from metabci.brainflow.workers import ProcessWorker



def send_command_to_serial(port, baudrate, command):
    try:
        # 打开串口
        ser = serial.Serial(port, baudrate, timeout=1)

        # 检查串口是否打开
        if ser.is_open:
            print(f'串口 {port} 已打开，波特率为 {baudrate}')

            # 发送命令
            ser.write(command.encode())
            print(f'已发送命令: {command}')

            # 关闭串口
            ser.close()
            print(f'串口 {port} 已关闭')
        else:
            print(f'无法打开串口 {port}')

    except Exception as e:
        print(f'发生错误: {e}')


def read_txt_file_periodically(file_path, interval=2):
    """
    每隔一定时间读取一次文本文件，并返回其内容。

    参数:
    file_path (str): 文本文件的路径。
    interval (int): 读取文件的时间间隔（秒）。

    返回:
    生成器: 每隔指定时间返回文件内容。
    """
    while True:
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read().strip()  # 读取文件内容并去除首尾空白
                number = int(content)  # 将内容转换为整数
            yield number
        except FileNotFoundError:
            yield f"文件未找到: {file_path}"
        except ValueError:
            yield "文件内容无法转换为整数"
        except Exception as e:
            yield f"读取文件时出错: {str(e)}"

        time.sleep(interval)

###柱体抓握
def output(input_value):
    if input_value == 1:
        command = 'C'
    else:
        command = 'R'
    return command




if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    w = ProcessWorker()
    w.show()
    E = app.exec_()
    if hasattr(w, 'thread1'):
        w.thread1.stop()
    if hasattr(w, 'outputSock'):
        w.outputSock.close()
    sys.exit(E)
