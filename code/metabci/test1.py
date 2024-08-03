from psychopy import monitors
import numpy as np
from brainstim.framework import Experiment

mon = monitors.Monitor(
    name='primary_monitor',
    width=59.6, distance=60,
    verbose=False
)
mon.setSizePix([1920, 1080])  # Resolution of the monitor
mon.save()
bg_color_warm = np.array([0, 0, 0])
win_size = np.array([1920, 1080])
# press esc or q to exit the start selection screen
ex = Experiment(
    monitor=mon,
    bg_color_warm=bg_color_warm,  # background of paradigm selecting interface[-1~1,-1~1,-1~1]
    screen_id=0,
    win_size=win_size,  # Paradigm border size (expressed in pixels), default[1920,1080]
    is_fullscr=True,  # True full window, then win_size parameter defaults to the screen resolution
    record_frames=False,
    disable_gc=False,
    process_priority='normal',
    use_fbo=False)
ex.register_paradigm(name, func, *args, **kwargs)