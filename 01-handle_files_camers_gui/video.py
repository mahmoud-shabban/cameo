import cv2

def main():
    file = './samples/videos/sample-2.mp4'
    
    video_capture = cv2.VideoCapture(file)
    
    fps = video_capture.get(cv2.CAP_PROP_FPS)
    
    size = (int(video_capture.get(cv2.CAP_PROP_FRAME_WIDTH)),
            int(video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    
    video_writer = cv2.VideoWriter(
        'MyOutputVid.mp4',
        cv2.VideoWriter_fourcc('M','P','4','V'),
        fps,
        size,
        True
    )
    
    success, frame = video_capture.read()
    
    while success:
        video_writer.write(frame)
        # success, frame = videoCapture.read()
if __name__ == '__main__':
    main()