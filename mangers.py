import time
import cv2 
import numpy

class PreviewWindowManager():
    pass
class CaptureManager(object):

    def __init__(self,
                 video_cpature: cv2.VideoCapture,
                 preview_window_manager:PreviewWindowManager = None,
                 should_mirror_preview: bool = False):
        
        self.preview_window_manager = preview_window_manager
        self.should_mirror_preview = should_mirror_preview
        self._capture  = video_cpature
        self._channel = 0
        self._entered_frame = False
        self._frame = None
        self._image_file_name = None
        self._video_file_name = None
        self._video_encoding = None 
        self._video_writer = None 
        self._start_time = None
        self._frames_elapsed = 0
        self._fps_estimte = None

    @property
    def channel(self):
        return self._channel
    
    @channel.setter
    def channel(self,value):
        if self._channel != value:
            self._channel = value
            self._frame = None

    @property
    def frame(self):
        if self._entered_frame and self._frame is None:
            _,self._frame = self._capture.retrive(
                self._frame, 
                self.channel
            )
        return self._frame
    
    @property
    def is_writing_image(self):
        return self._image_file_name is not None
    @property
    def is_writing_video(self):
        return self._video_file_name is not None
    
    def enter_frame(self):
        '''capture the next frame if any''' # but first check if any previeous frame existed
        assert not self._entered_frame, \
        'previous enter_frame() had no matching exit_frame()'
        
        if self._capture is not None:
            self._entered_frame = self._capture.grab()

    def exit_frame(self):
        '''Draw to the window. Write to files. Release the frame.'''
        if self.frame is None:
            self._entered_frame = False
            return
        if self._frames_elapsed == 0:
            self._start_time = time.perf_counter()
        else:
            time_elapsed = time.perf_counter() - self._start_time
            self._fps_estimte = self._frames_elapsed / time_elapsed
        
        self._frames_elapsed += 1

        if self.preview_window_manager is not None:
            if self.should_mirror_preview:
                mirrored_frame = numpy.fliplr(self._frame)
                self.preview_window_manager.show(mirrored_frame)
            else:
                self.preview_window_manager.show(self._frame)
        
        if self.is_writing_image:
            cv2.imwrite(self._image_file_name, self._frame)
            self._image_file_name = None 
        self._write_video_frame()
        self._frame = None
        self._entered_frame = False

cm = CaptureManager()
