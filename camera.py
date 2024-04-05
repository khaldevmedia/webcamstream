#STD
import threading

# Installed libraries
import cv2

class VideoCamera():
    def __init__(self):
        self.video = cv2.VideoCapture(0) # for most systems 0 would refer to the defaut built-in camera. Select 1, 2 etc  if you have multiple cameras
        self.lock = threading.Lock() #  to ensure that each frame is fully read and encoded before another thread (user) can access the VideoCapture object


    def __del__(self):
        self.video.release()
        

    def get_frame(self):
        
        ret, frame = self.video.read() # ret is a successful flag to hep debug
        ## Uncomment this line if you want to adjust alpha (contrast) and beta (brightness) of the image
        # frame = cv2.convertScaleAbs(frame, alpha = 1.1, beta = 0.9)
        ret, jpeg = cv2.imencode('.jpg', frame)
        return jpeg.tobytes()
