from IPython.display import HTML, display
from tempfile import NamedTemporaryFile
from matplotlib import pyplot as plt
from matplotlib import animation
import base64

import abc


class IPythonChartAnimation(object):
    __metaclass__ = abc.ABCMeta

    VIDEO_TAG = """<video controls>
                 <source src="data:video/x-m4v;base64,{0}" type="video/mp4">
                 Your browser does not support the video tag.
                </video>"""

    def __init__(self):
        pass

    def __anim_to_html(self, animation, fps):
        if not hasattr(animation, '_encoded_video'):
            with NamedTemporaryFile(suffix='.mp4') as f:
                animation.save(f.name, fps=fps, extra_args=['-vcodec', 'libx264'])
                video = open(f.name, "rb")
            animation._encoded_video = base64.b64encode(video.read())

        return self.VIDEO_TAG.format(animation._encoded_video)

    def __display_animation(self, anim, fps):
        plt.close(anim._fig)
        return HTML(self.__anim_to_html(anim, fps))

    @abc.abstractmethod
    def _init_animation(self):
        raise NotImplementedError()

    def _start_animation(self, animation_callback, init_animation_callback,
                         target_canvas, frames=100, interval=20, fps=10):

        animation_handle = animation.FuncAnimation(target_canvas, animation_callback,
                                                   init_func=init_animation_callback,
                                                   frames=frames, interval=interval, blit=True)
        return display(self.__display_animation(animation_handle, fps))

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

