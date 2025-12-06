import cv2 
from managers import WindowManager, CaptureManager 

class Cameo(object):
    def __init__(self):
        self._windowManager = WindowManager('Cameo',
                                            self.on_key_press)
        self._captureManager = CaptureManager(
            cv2.VideoCapture(0),
            self._windowManager,
            True
        )

    def run(self):
        '''run the main loop'''
        
        self._windowManager.create_window()
        
        while self._windowManager.is_window_created:
            self._captureManager.enter_frame()
            frame = self._captureManager.frame
            
            if frame is not None:
                pass 
            
            self._captureManager.exit_frame()
            self._windowManager.process_events()
    
    def on_key_press(self, key_code):
        '''
        handle a key press.
            space -> take a screenshot
            tab -> start/stop recording a screencast
            escape -> quit
        '''

        if key_code == 32: #Space
            self._captureManager.write_image('screenshot.png')
        elif key_code == 9: # Tab
            print("keypress callback on TAB")
            if not self._captureManager.is_writing_video: 
                self._captureManager.start_writing_video(
                    'screencast.avi')
            else:
                self._captureManager.stop_writing_video()
        elif key_code == 27: # Escape
            self._windowManager.destroy_window()


if __name__=='__main__':
    Cameo().run()