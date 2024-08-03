import cv2
import tkinter as tk
from PIL import Image, ImageTk
import pygame
import argparse
import numpy as np
import serial.tools.list_ports
from brainflow.board_shim import BoardShim, BrainFlowInputParams
from brainflow.data_filter import DataFilter
# from OnlineProcessor import OnlineProcessor  # 假设 onlineprocesser 定义在 onlineprocesser.py 文件中
from metabci.brainflow.workers import ProcessWorker

data_all = []

def detect_serial_port():
    """ 检测当前使用的串口 """
    ports = serial.tools.list_ports.comports()
    for port in ports:
        if "USB" in port.description:  # 根据需要调整匹配条件
            return port.device
    return None  # 如果未找到匹配的端口，则返回 None 或者其他适当的值

class VideoPlayer:
    def __init__(self, video_file, voice_file, num_loops, online_processor):
        self.video_file = video_file
        self.voice_file = voice_file
        self.num_loops = num_loops
        self.online_processor = online_processor
        self.loop_count = 0
        self.cap = None
        self.root = tk.Tk()
        self.label = tk.Label(self.root)
        self.data = []
        self.label.pack()
        self.root.protocol("WM_DELETE_WINDOW", self.close)

    def run(self):
        self.cap = cv2.VideoCapture(self.video_file)
        # 加载音频
        pygame.mixer.init()
        pygame.mixer.music.load(self.voice_file)
        pygame.mixer.music.set_volume(1.0)
        # pygame.mixer.music.play()
        self.show_frame()
        self.root.mainloop()

    def show_frame(self):
        ret, frame = self.cap.read()

        if ret:
            rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            pil_image = Image.fromarray(rgb_image)
            tk_image = ImageTk.PhotoImage(image=pil_image)
            self.label.configure(image=tk_image)
            self.label.image = tk_image
        else:
            pygame.mixer.music.play()
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)  # 重新播放视频
            # pygame.mixer.music.play()
            # data_all.extend(self.data)
            self.loop_count += 1

            if self.loop_count >= self.num_loops:
                pygame.mixer.music.pause()
                self.cap.release()
                self.close()
                self.data = self.online_processor.thread1.get_bufferData()  # 获取脑电数据
                np.save('data_EEG.npy', self.data)
                self.online_processor.board.release_session()
                return

        self.root.after(18, self.show_frame)

    def close(self):
        self.root.destroy()
        # self.board.stop_stream()
        # self.board.release_session()

def start_video_player(num_loops):
    video_file = "validate_video.mp4"  # 视频文件名
    voice_file = "ding.wav"
    BoardShim.enable_dev_board_logger()
    parser = argparse.ArgumentParser()
    parser.add_argument('--timeout', type=int, help='timeout for device discovery or connection', required=False, default=0)
    parser.add_argument('--board-id', type=int, help='board id, check docs to get a list of supported boards', required=False, default=0)
    parser.add_argument('--file', type=str, help='file', required=False, default=0)
    parser.add_argument('--master-board', type=int, help='master board id for streaming and playback boards', required=False, default=-1)
    parser.add_argument('--streamer-params', type=str, help='streamer params', required=False, default='')
    parser.add_argument('--other-info', type=str, help='other info', required=False, default='-1')
    args = parser.parse_args()
    params = BrainFlowInputParams()
    params.serial_port = detect_serial_port()
    params.file = args.file
    params.other_info = args.other_info
    board = BoardShim(args.board_id, params)
    board.prepare_session()
    online_processor = ProcessWorker(board)  # 实例化 onlineprocesser
    player = VideoPlayer(video_file, voice_file, num_loops, online_processor)
    board.start_stream()
    player.run()

def create_interface():
    root = tk.Tk()
    label = tk.Label(root, text="请输入校验次数：")
    label.pack()
    entry = tk.Entry(root)
    entry.pack()
    button = tk.Button(root, text="运行", command=lambda: run_program(entry.get(), root))
    button.pack()
    root.mainloop()

def run_program(num_loops, root):
    num_loops = int(num_loops)
    root.destroy()
    start_video_player(num_loops)

if __name__ == "__main__":
    create_interface()
