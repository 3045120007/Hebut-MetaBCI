# 作者：王泾宇
# 开发日期：2024/6/24
'''
程序功能说明：
    1、选择串口
    2、选择波特率
    3、给串口发送字符指令
'''
import serial
import time

import time
import serial


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


def output(input_value):
    if input_value == 1:
        command = 'B'
    else:
        command = 'R'
    return command


# 示例使用
if __name__ == '__main__':
    port = 'COM6'  # 请根据你的情况更改串口号，例如 'COM3' 或 '/dev/ttyUSB0'
    baudrate = 9600  # 设置波特率

    file_path = 'outputvideo.txt'
    number_reader = read_txt_file_periodically(file_path)

    for number in number_reader:
        print(f'读取的值: {number}')

        if isinstance(number, int):
            command = output(number)
            send_command_to_serial(port, baudrate, command)
        else:
            print(number)  # 打印错误信息或其他非整数内容

        time.sleep(0.5)  # 每次读取和发送命令后等待5秒
