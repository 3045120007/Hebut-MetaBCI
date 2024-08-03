
# @ 14th August 2018
# FANG Junying
#!/usr/bin/env python3
#-*- coding:utf-8 -*-

import socket
from struct import unpack
import numpy as np
from  threading import Timer,Lock, Thread, Event
import select,time
# import matplotlib.pyplot as plt


def  ParseDataNeuracle(data,n_chan,fmt ='<f'):
    n_item = int(len(data)/n_chan/4)
    parse_data = [[] for _ in range(n_chan)]
    for j in range(n_chan):
        for i in range(n_item):
             st,stp = (i*n_chan+j)*4, (i*n_chan+j)*4 + 4
             if j == n_chan-1:
                 parse_data[j].append(unpack('<i', data[st:stp])[0])
             else:
                 parse_data[j].append(unpack(fmt, data[st:stp])[0])
    return np.asarray(parse_data)

def ParseDataWS():
    pass



class ringBuffer():
    def __init__(self,n_chan,n_points):
        self.n_chan = n_chan
        self.n_points = n_points
        self.buffer = np.zeros((n_chan, n_points))
        self.currentPtr = 0
        self.nUpdate = 0
    def appendBuffer(self,data):
        n = data.shape[1]
        self.buffer[:,np.mod(np.arange(self.currentPtr,self.currentPtr+n),self.n_points)] = data
        self.currentPtr = np.mod(self.currentPtr+n-1, self.n_points) + 1
        self.nUpdate = self.nUpdate+n

    def getData(self):
        data = np.hstack([self.buffer[:,self.currentPtr:], self.buffer[:,:self.currentPtr]])
        return data
    def resetBuffer(self):
        self.buffer = np.zeros((self.n_chan, self.n_points))
        self.currentPtr = 0
        self.nUpdate = 0

class dataserver_thread(Thread,):
    def __init__(self,threadName,device,n_chan, hostname='127.0.0.1', port= 8712,srate=1000,t_buffer=3):
        Thread.__init__(self)
        self.name = threadName
        self.sock = []
        self.device = device
        self.n_chan = n_chan
        self.hostname = hostname
        self.port = port
        self.t_buffer = t_buffer
        self.srate = srate
        self._update_interval = 0.04


    def connect(self):
        """
        connect(hostname [, port]) -- make a connection, default port is
        """
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        notconnect = True
        reconnecttime = 0
        while notconnect:
            try:
                self.sock.connect((self.hostname, self.port))
                print('DataServer Connection Successfully')
                notconnect = False
            except:
                reconnecttime += 1
                print('connection failed, retrying for %d times\n' % reconnecttime)
                time.sleep(1)
                if reconnecttime > 10:
                    print('Connection Failed')
                    break
        self.shutdown_flag = Event()
        self.shutdown_flag.set()
        # self.sock.setblocking(True)
        self.bufsize = int(self._update_interval*4*self.n_chan*self.srate*10)
        self.npoints_buffer = int(np.round(self.t_buffer*self.srate))
        self.ringBuffer = ringBuffer(self.n_chan, self.npoints_buffer)
        self.buffer = b''

    def run(self):
        self.read_thread()

    def read_thread(self):
        socket_lock = Lock()
        while self.shutdown_flag.isSet():
            if not self.sock:
                break
            rs, _, _ = select.select([self.sock], [], [], 9)
            for r in rs:
                socket_lock.acquire()
                if not self.sock:
                    socket_lock.release()
                    break
                try:
                    raw = r.recv(self.bufsize)
                except:
                    print('不能抓取数据。。。。')
                    socket_lock.release()
                    self.sock.close()
                else:
                    raw = self.buffer + raw
                    data, evt = self.parseData(raw)
                    socket_lock.release()

                    data = data.reshape(len(data) // (self.n_chan), self.n_chan)
                    self.ringBuffer.appendBuffer(data.T)
                    # print(self.ringBuffer.nUpdate)


                    # print('Server Closed')
                    # self.connect() # try connect again

                    # if len(data) > 0:
                    #     data = data.reshape(len(data) // (self.n_chan), self.n_chan)
                    #     self.ringBuffer.appendBuffer(data.T)
                    #     # print(self.ringBuffer.nUpdate)
                    #
                    # else:
                    #     print('Server Closed')
                    #     self.connect() # try connect again

    def parseData(self,raw):
        if 'Neuracle' in self.device:
            n = len(raw)
            event , hexData  = [], []
            hexData = raw[:n - np.mod(n, 4 * self.n_chan)] # unpack hex-data  in row
            self.buffer = raw[n - np.mod(n, 4 * self.n_chan):]
            n_item = int(len(hexData)/4/self.n_chan)
            format_str = '<' + (str(self.n_chan -1) + 'f' + '1I') * n_item
            parse_data = unpack(format_str, hexData)

        elif 'DSI-24' in self.device:
            token = '@ABCD'
            n = len(raw)
            i = 0
            parse_data, data_record, event, event_record  = [], [], [], []
            iData = 0
            iEvent = 1
            while i + 12 < n:
                if token == raw[i:i + 5].decode('ascii'):
                    packetType = raw[i + 5]
                    # print(packetType)
                    bytenum = raw[i + 6:i + 8]
                    packetLength = 256 * bytenum[0] + bytenum[1]
                    # bytenum = unpack('>4I', raw[i+8:i+12])
                    # packetNumber = 16777216*bytenum[0]+65536*bytenum[1]+256*bytenum[2]+bytenum[3]
                    if i + 12 + packetLength > n:
                        break
                    if packetType == 1:
                        data_record.append({})
                        # bytenum = unpack('>4I', raw[i+12:i+16])
                        # data_record[iData]['TimeStamp'] = 16777216*bytenum[0]+65536*bytenum[1]+256*bytenum[2]+bytenum[3]
                        # data_record[iData]['DataCounter'] = unpack('>I', raw[i+16])
                        # data_record[iData]['ADCStatus'] = unpack('>I', raw[i+17:i+23])[0]
                        # if np.mod(packetLength - 11, 4) != 0:
                        #     print('The packetLength may be incorrect!')
                        # else:
                        #     pass
                        data_num = int((packetLength - 11) / 4)
                        format = '>' + str(data_num) + 'f'
                        data_record[iData]['ChannelData'] = unpack(format, raw[i + 23:i + 12 + packetLength])
                        parse_data.extend(data_record[iData]['ChannelData'])
                        iData += 1
                    elif packetType == 5:
                        event_record.append({})
                        # bytenum = unpack('>4I', raw[i+12:i+16])
                        # event_record[iEvent]['EventCode'] = 16777216*bytenum[0]+65536*bytenum[1]+256*bytenum[2]+bytenum[3]
                        # bytenum = unpack('>4I', raw[i+16:i+20])
                        # event_record[iEvent]['SendingNode'] = 16777216*bytenum[0]+65536*bytenum[1]+256*bytenum[2]+bytenum[3]
                        # if packetLength > 20:
                        #     bytenum = unpack('>4I', raw[i+20:i+24])
                        #     event_record[iEvent]['MessageLength'] = 16777216*bytenum[0]+65536*bytenum[1]+256*bytenum[2]+bytenum[3]
                        #     event_record[iEvent]['Message'] = raw[i+24:i+24+event[iEvent]['MessageLength']].decode('ascii')
                        # event.extend(event_record[iEvent]['Message'])
                        # iEvent += 1
                    else:
                        pass
                    i = i + 12 + packetLength
                else:
                    i += 1
            self.buffer = raw[i:]
        else:
            print('not avaliable device !')
            parse_data =[]
            event = []
            pass
        return np.asarray(parse_data), event


    def get_bufferData(self):
        return self.ringBuffer.getData()

    def stop(self):
        self.shutdown_flag.clear()


if __name__ == '__main__':
    thread1 = dataserver_thread(threadName='thread_dataServer', device='Neuracle', n_chan=10,hostname='127.0.0.1')
    thread1.Daemon = True
    thread1.connect()
    thread1.start()
    thread1.join()






































#
# def start_client(ADDR,BUFFSIZE):
#     n_chan, srate, update_interval = 10, 1000.0, 0.04
#     sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     sock.connect(ADDR)
#     # read_thread_method(sock, BUFFSIZE)
#     global timer
#     timer = Timer(0.003, read_thread_method,(sock, BUFFSIZE))
#     timer.start()
#     print('****************************')
#
# def read_thread_method(sock,BUFFSIZE):
#     # HOST ='localhost'
#     # PORT = 8712
#     n_chan, srate, update_interval = 10, 1000.0, 0.04
#     # BUFFSIZE=int(update_interval*4*n_chan*srate*10)
#     # n_chan, srate, update_interval = 10, 1000.0, 0.04
#     # sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     # sock.connect(ADDR)
#     # data = sock.recv(BUFFSIZE)
#     socket_lock = Lock()
#     while True:
#         if not sock:  # 如果socket关闭，退出
#             break
#     # 使用select监听客户端（这里客户端需要不停接收服务端的数据，所以监听客户端）
#         rs, _, _ = select.select([sock], [], [], 2)
#         print(rs)
#         for r in rs:  # 我们这里只监听读事件，所以只管读的返回句柄数组
#             socket_lock.acquire()  # 在读取之前先加锁，锁定socket对象（sock是主线程和子线程的共享资源，锁定了sock就能保证子线程在使用sock时，主线程无法对sock进行操作）
#             if not sock:  # 这里需要判断下，因为有可能在select后到加锁之间socket被关闭了
#                 socket_lock.release()
#                 break
#             data = r.recv(BUFFSIZE)  # 读数据，按自己的方式读
#             parse_data = parse_socket_data(data, n_chan)
#             socket_lock.release()  # 读取完成之后解锁，释放资源
#             if not data:
#                 print( 'server close')
#             else:
#                 print('-----------------finish-------------------')
#                 print('-----------------finish-------------------')
#                 print('-----------------finish-------------------')
#                 print (np.shape(parse_data ))
#         # time.sleep(1)
#
#
#     # for i in range(1000000000000000000 ):
#     #     sum = sum + i
#     #     print(i)
#
#     # HOST ='localhost'
#     # PORT = 8712
#     # n_chan, srate, update_interval = 10, 1000.0, 0.04
#     # BUFFSIZE=int(update_interval*4*n_chan*srate*10)
#     # ADDR = (HOST,PORT)
#     # # 创建套接字
#     # tctimeClient = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
#     # #向服务器发送连接请求
#     # tctimeClient.connect(ADDR)
#     # read_thread_method(tctimeClient)
#     # read_thread = Thread(target=read_thread_method,name='client scoket thread')
#     # read_thread.setDaemon(True)
#     # read_thread.start()
#
#
#     # timer = Timer(1, read_thread_method)
#     # timer.start()
#     # print('already started the client thread')
#     # print('-----------------finish-------------------')
#     # sum=0
#     # for i in range(100 ):
#     #     sum = sum + i
#     #     print(i)
#
#
#     # time.sleep(10)
#     # timer.cancel()
#     # #
#     # # 和服务器端进行通信(send/receive) 接收数据
#     # socket_data = tctimeClient.recv(BUFFSIZE)
#     # # 解析16进制data
#     # data = parse_socket_data(socket_data,n_chan)
#     # # 关闭套接字
#     # tctimeClient.close()
#     # print(np.shape(data))
#     # # timer=Timer(1, timer_callback)
#     # # timer.start()
