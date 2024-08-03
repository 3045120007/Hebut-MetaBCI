# """
# 时间：
#     2023年12月17日 11:00:00
# 作者：
#     李钧迪
# 内容：
#     视频播放功能改变为：正常速度、加速、倒放
#
# 说明1---conconet.py：
#     1、视频播放功能：慢速、正常速度、加速
#     2、generate_speed中的speed量进行修改，通过更新speed改变视频播放的功能
#     3、视频和py文件放置于同一个文件夹下
#     4.数字越大视频播放越慢，越小越快
#
# 说明2--inverse.py：
#     1、视频播放功能：倒放、正常速度、加速
#     2、generate_speed中的speed量进行修改，通过更新speed改变视频播放的功能
#     3、视频和py文件放置于同一个文件夹下
#     4.数字越大视频播放越慢，越小越快
#     5.设置playvideo中的if语句模块对倒放进行修改
# """
# import time
# import random
# import threading
# import queue
# import cv2
# import tkinter as tk
# from PIL import Image, ImageTk
# def read_value_from_txt(filename='output.txt'):
#     # 打开文件并以读取模式打开
#     with open(filename, 'r') as file:
#         # 读取文件中的值
#         value = file.read()
#         # 将字符串转换为相应的数据类型，如果需要的话
#         # 这取决于你保存到文件中的数据类型
#
#     return value
# class VideoPlayer:
#     def __init__(self, video_path):
#         self.video_path = video_path
#         self.speed_queue = queue.Queue()
#         self.current_speed = 0
#         self.reverse = False  # 是否倒放视频
#
#         # 创建一个Tkinter窗口
#         self.window = tk.Tk()
#         self.window.title("视频播放器")
#
#         # 创建一个标签用于显示视频帧
#         self.video_label = tk.Label(self.window)
#         self.video_label.pack()
#
#         # 打开视频文件
#         self.video_capture = cv2.VideoCapture(video_path)
#
#         # 启动速度生成线程
#         speed_thread = threading.Thread(target=self._generate_speed)
#         speed_thread.daemon = True
#         speed_thread.start()
#
#         # 启动速度更新线程
#         speed_update_thread = threading.Thread(target=self._update_speed)
#         speed_update_thread.daemon = True
#         speed_update_thread.start()
#
#         # 启动视频播放线程
#         video_play_thread = threading.Thread(target=self._play_video)
#         video_play_thread.daemon = True
#         video_play_thread.start()
#
#         # 启动Tkinter事件循环
#         self.window.mainloop()
#
#     # 生成随机速度并将其放入队列中，每5秒传递一次
#     # def _generate_speed(self):
#     #     while True:
#     #         speed = random.choice([3, 2])
#     #         self.speed_queue.put(speed)
#     #         time.sleep(0.5)
#     def _generate_speed(self):
#         while True:
#             speed = read_value_from_txt(filename='outputvideo.txt')
#             speed = int(speed)
#             # speed = random.choice([5, 3, 2])
#             self.speed_queue.put(speed)
#             time.sleep(1)
#     # 从队列中获取速度并更新当前播放速度
#     def _update_speed(self):
#         while True:
#             speed = self.speed_queue.get()
#             self.current_speed = speed
#
#     # 播放视频的函数
#     def _play_video(self):
#         while True:
#             # 读取视频帧
#             ret, frame = self.video_capture.read()
#
#             if not ret:
#                 break
#
#             # 根据当前速度调整视频播放速度，调整倒放的条件
#             if self.current_speed == 0:  # 当速度为1时
#                 self.reverse = True  # 切换为倒放状态
#             else:
#                 self.reverse = False  # 切换为正放状态
#
#
#
#             # 将OpenCV图像转换为Tkinter图像
#             frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#             image = Image.fromarray(frame_rgb)
#             image_tk = ImageTk.PhotoImage(image)
#
#             # 在标签中显示图像
#             self.video_label.config(image=image_tk)
#             self.video_label.image = image_tk
#
#             # 设置视频播放速度为每帧间隔的毫秒数
#             interval = int(1000 / self.video_capture.get(cv2.CAP_PROP_FPS) * self.current_speed)
#             # print(self.current_speed)
#
#             # 更新界面
#             self.window.update()
#
#             # 按照间隔时间延迟下一帧
#             time.sleep(interval / 1000)
#             if self.reverse:  # 如果处于倒放状态
#                 self.video_capture.set(cv2.CAP_PROP_POS_FRAMES, self.video_capture.get(cv2.CAP_PROP_POS_FRAMES) - 2)
#
# # 示例用法
# if __name__ == '__main__':
#     # 创建VideoPlayer实例
#     player = VideoPlayer('movie4.mp4')
#
#
# def inverse():
#     VideoPlayer('movie4.mp4')

import time
import random
import threading
import queue
import cv2
import tkinter as tk
from PIL import Image, ImageTk
def read_value_from_txt(filename='output.txt'):
    # 打开文件并以读取模式打开
    with open(filename, 'r') as file:
        # 读取文件中的值
        value = file.read()
        # 将字符串转换为相应的数据类型，如果需要的话
        # 这取决于你保存到文件中的数据类型
    return value

class VideoPlayer:
    def __init__(self, video_path):
        self.video_path = video_path
        self.speed_queue = queue.Queue()
        self.current_speed = 1
        self.reverse = False  # 是否倒放视频
        self.paused = False  # 是否暂停视频
        self.last_frame = None  # 上一帧图像

        # 打开视频文件
        self.video_capture = cv2.VideoCapture(video_path)

        # 读取视频帧并缓存
        self.frames = []
        while True:
            ret, frame = self.video_capture.read()
            if not ret:
                break
            self.frames.append(frame)

        # 创建一个Tkinter窗口
        self.window = tk.Tk()
        self.window.title("视频播放器")

        # 创建一个标签用于显示视频帧
        self.video_label = tk.Label(self.window)
        self.video_label.pack()

        # 启动速度生成线程
        speed_thread = threading.Thread(target=self._generate_speed)
        speed_thread.daemon = True
        speed_thread.start()

        # 启动速度更新线程
        speed_update_thread = threading.Thread(target=self._update_speed)
        speed_update_thread.daemon = True
        speed_update_thread.start()

        # 启动视频播放线程
        video_play_thread = threading.Thread(target=self._play_video)
        video_play_thread.daemon = True
        video_play_thread.start()

        # 启动Tkinter事件循环
        self.window.mainloop()

    # 生成随机速度并将其放入队列中，每5秒传递一次
    def _generate_speed(self):
        while True:
            speed = read_value_from_txt(filename='outputvideo.txt')
            speed = int(speed)
            # speed = random.choice([5, 3, 2])
            self.speed_queue.put(speed)
            time.sleep(2)

    # 从队列中获取速度并更新当前播放速度
    def _update_speed(self):
        while True:
            speed = self.speed_queue.get()
            self.current_speed = speed

    def _play_video(self):
        frame_index = 0  # 当前帧的索引
        self.last_frame = self.frames[frame_index]  # 显示第一帧图像
        frame_index += 1  # 增加帧索引
        while True:
            # 根据当前速度调整视频播放速度和暂停状态
            if self.current_speed == 0:  # 当速度为0时
                self.paused = True  # 暂停视频
            else:
                self.paused = False  # 继续播放视频
            print(self.current_speed)

            if not self.paused:  # 如果视频没有暂停
                # 获取当前帧
                frame = self.frames[frame_index]

                # 将OpenCV图像转换为Tkinter图像
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                image = Image.fromarray(frame_rgb)
                image_tk = ImageTk.PhotoImage(image)

                # 在标签中显示图像
                self.video_label.config(image=image_tk)
                self.video_label.image = image_tk

                # 设置视频播放速度为每帧间隔的毫秒数
                interval = int(300 / self.video_capture.get(cv2.CAP_PROP_FPS) * self.current_speed)

                # 更新界面
                self.window.update()

                # 按照间隔时间延迟下一帧
                time.sleep(interval / 300)

                # 更新帧索引
                if not self.reverse:  # 正放播放
                    frame_index = (frame_index + 1) % len(self.frames)
                else:  # 倒放播放
                    frame_index = (frame_index - 1) % len(self.frames)
                    # frame_index = frame_index%len(self.frames)

                self.last_frame = frame
            else:
                # 暂停时显示上一帧图像
                if self.last_frame is not None:
                    frame_rgb = cv2.cvtColor(self.last_frame, cv2.COLOR_BGR2RGB)
                    image = Image.fromarray(frame_rgb)
                    image_tk = ImageTk.PhotoImage(image)
                    self.video_label.config(image=image_tk)
                    self.video_label.image = image_tk

# 示例用法
if __name__ == '__main__':
    # 创建VideoPlayer实例
    player = VideoPlayer('green.mp4')


def green_play():
    VideoPlayer('green.mp4')