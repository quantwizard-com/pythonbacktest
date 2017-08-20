from IPython.display import display
from matplotlib import animation, rc

import abc


class IPythonChartAnimation(object):
    __metaclass__ = abc.ABCMeta

    VIDEO_TAG = """<video controls>
                 <source src="data:video/x-m4v;base64,{0}" type="video/mp4">
                 Your browser does not support the video tag.
                </video>"""

    def __init__(self):
        self.__target_canvas = None
        self.__number_of_frames = None
        self.__interval = None

    @abc.abstractmethod
    def _init_animation(self):
        raise NotImplementedError()

    def _start_animation(self, animation_callback, init_animation_callback,
                         target_canvas, frames=100, interval=200):

        anim = animation.FuncAnimation(target_canvas, animation_callback,
                                                   init_func=init_animation_callback,
                                                   frames=frames, interval=interval, blit=True)

        rc('animation', html='html5')
        display(anim)

    @property
    def target_canvas(self):
        return self.__target_canvas

    @target_canvas.setter
    def target_canvas(self, canvas):
        self.__target_canvas = canvas

    @property
    def number_of_frames(self):
        return self.__number_of_frames

    @number_of_frames.setter
    def number_of_frames(self, value):
        self.__number_of_frames = value

    @property
    def interval(self):
        return self.__interval

    @interval.setter
    def interval(self, inter):
        self.__interval = inter

