import cv2
import numpy as np
class pFrameData:
    def __init__(self,filepath,window_size,step = 10):
        self.window_size = window_size
        self.file = filepath
        self.step = step
    def __next__(self):
        count = 0
        flag = False
        if self.file.split(".")[-1] in "avi.mp4".split('.'):
            print(self.file.split(".")[-1])
            cap = cv2.VideoCapture(self.file)
            print(cap.isOpened())
            mainCounter = -1
            if cap.isOpened():
                while True:
                    mainCounter += 1
                    frames = np.empty([0,320,320,3],dtype = np.float32)
                    while not count or count%self.window_size != 0:
                        flag,frame = cap.read()
                        cap.set(cv2.CAP_PROP_POS_FRAMES,self.step+mainCounter)
                        print(flag)
                        if flag:
                            frame = cv2.resize(frame,(320,320))
                            frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
                            frame = np.float32(frame)/np.float32(max(frame.flatten()))
                            frames = np.append(frames,frame.reshape([1]+list(frame.shape[:])),axis = 0)
                            count += 1
                            print(frames.shape)
                        else:
                            break
                    if not flag:
                        break
                    else:
                        return frames
                    
        elif self.file.split(".")[-1] in "jpg.png".split('.'):
            print(self.file.split(".")[-1])
            frame = cv2.imread(self.file)
            frame = cv2.resize(frame,(320,320))
            frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
            frame = np.float32(frame)/np.float32(max(frame.flatten()))
            return np.expand_dims(frame,axis = 0)
