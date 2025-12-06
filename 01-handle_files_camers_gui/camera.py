import cv2

def main():
    cameraCapture = cv2.VideoCapture(0)

    fps = 30 # An assumption
    
    size = (int(cameraCapture.get(cv2.CAP_PROP_FRAME_WIDTH)),
        int(cameraCapture.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    
    videoWriter = cv2.VideoWriter(
        'MyOutputVid.avi', cv2.VideoWriter_fourcc('I','4','2','0'),
        fps, size)
    
    if cameraCapture.isOpened():
        success, frame = cameraCapture.read()
    
        numFramesRemaining = 10 * fps - 1 # 10 seconds of frames
        # numFramesRemaining = 10 * fps
        while success and numFramesRemaining >0:
            # do any job on the frame before writing it down
            #
            #######
            videoWriter.write(frame)
            success, frame = cameraCapture.read()
            numFramesRemaining -= 1


if __name__ == '__main__':
    main()