# 作者：王泾宇
# 开发日期：2024/6/24
'''
程序功能说明：
    1、选择串口
    2、选择波特率
    3、给串口发送字符指令
'''
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

# 示例使用
if __name__ == '__main__':
    port = 'COM6' # 请根据你的情况更改串口号，例如 'COM3' 或 '/dev/ttyUSB0'
    baudrate = 9600 # 设置波特率
    command = 'R' # 你的单字符命令

    send_command_to_serial(port, baudrate, command)