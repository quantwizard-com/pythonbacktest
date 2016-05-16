from IPython.display import HTML
from tempfile import NamedTemporaryFile
from matplotlib import pyplot as plt
from matplotlib import animation

import abc


# this is baseclass for all classes, which intend to render animation
# within IPython notebook
class IPythonAnimation(object):
    __metaclass__ = abc.ABCMeta

    VIDEO_TAG = """<video controls>
                 <source src="data:video/x-m4v;base64,{0}" type="video/mp4">
                 Your browser does not support the video tag.
                </video>"""

    def __init__(self, frames=100, interval=20):
        self.__target_canvas = plt.figure()
        self.__number_of_frames = frames
        self.__interval = interval

    def __anim_to_html(self, animation):
        if not hasattr(animation, '_encoded_video'):
            with NamedTemporaryFile(suffix='.mp4') as f:
                animation.save(f.name, fps=20, extra_args=['-vcodec', 'libx264'])
                video = open(f.name, "rb").read()
            animation._encoded_video = video.encode("base64")

        return self.VIDEO_TAG.format(animation._encoded_video)

    def __display_animation(self, anim):
        plt.close(anim._fig)
        return HTML(self.__anim_to_html(anim))

    @abc.abstractmethod
    def _init_animation(self):
        raise NotImplementedError()

    @abc.abstractmethod
    def _animate_callback(self, animation_parameter):
        raise NotImplementedError()

    def start_animation(self):
        animation_handle = animation.FuncAnimation(self.target_canvas, self._animate_callback,
                                                   init_func=self._init_animation,
                                                   frames=self.__number_of_frames, interval=self.__interval, blit=True)
        self.__display_animation(animation_handle)

    @property
    def target_canvas(self):
        return self.__target_canvas

    @property
    def number_of_frames(self):
        return self.__number_of_frames

    @number_of_frames.setter
    def number_of_frames(self, value):
        self.__number_of_frames = value

    @property
    def interval(self):
        return self.__interval

