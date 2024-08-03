from metabci.brainstim.report import *
from metabci.brainstim.massage import *
from metabci.brainstim.htmll import *
from metabci.brainstim.start_ti import *
from metabci.brainstim.online_test import *
from metabci.brainstim.green_play import *
from metabci.brainstim.fly_play import *
import threading
from metabci.brainstim.loading import *

# from report import *
# from massage import *
# from htmll import *
# from start_ti import *
# from online_test import *
# from green_play import *
# from fly_play import *
# import threading
# from loading import *

sle=2.6
from closee import *

start_ti()
#调用输入信息界面 输入信息界面出现
name,gender,age,experiment_count=massage()
# name,gender,age=massage()
#建立线程
if(experiment_count=="1"):
    player_thread = threading.Thread(target=fly_play)
else:
    player_thread = threading.Thread(target=green_play)

plot_thread = threading.Thread(target=plot_video2)
#线程开始
plot_thread.start()
loading()
#由于实时脑电需要初始化，所以先休眠2.6s保证窗口同时出现
player_thread.start()
player_thread.join()
#调用结果展示界面 结果展示界面出现
htmll(name,gender,age, "报告内容")
report(name,gender,age, "报告内容")
# htmll(name,gender,age, experiment_count,"报告内容")
# report(name,gender,age, experiment_count,"报告内容")
#输出网页版报告
