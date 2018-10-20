import cv2
import os
import random
import logger
import glob
import numpy as np
class FrameData:
    def __init__(self,video_folder,type_ = None,window_size = None,frame_step = 5,dim =(None,None),normalize = True,dtype = np.float32):
        self.window_size = window_size
        self.log = logger.Log("FRAMES")
        self.frame_step = frame_step
        self.type_ =type_
        video_folder = os.path.abspath(os.path.expanduser(video_folder))
        if video_folder[-1]!="/":
        	video_folder += "/"
        s_ftypes = "*.mp4 *.avi".split(" ")
        try:
            os.listdir(video_folder+"pos")
            os.chdir(video_folder+"pos")
        except FileNotFoundError:
            self.log.log(logger.critical,"Need a folder named pos containing the positive videos")
            raise
        posFiles = []
        for e in s_ftypes:
            posFiles.extend(glob.glob(e))
        os.chdir("..")
        if len(posFiles)==0:
            self.log.log(logger.critical,"Supported Video File(s) [mp4, avi] Not Found in pos/ folder")
        try:
            os.listdir(video_folder+"neg")
            os.chdir(video_folder+"neg")
        except FileNotFoundError:
            self.log.log(logger.critical,"Need a folder named neg containing the positive videos")
            raise
        negFiles = []
        for e in s_ftypes:
            negFiles.extend(glob.glob(e))

        if len(negFiles)==0:
            self.log.log(logger.critical,"Supported Video File(s) [mp4, avi] Not Found in pos/ folder")
        os.chdir("..")
        self.cwd = video_folder
        self.dtype = dtype
        if (dim[0] and dim[1]) or not (dim[0] and dim[1]):
            self.dim = dim
        else:
            raise ValueError("The target dimensions can only have numbers or None as the (width,height)")
        self.negFiles = negFiles[:]
        self.posFiles = posFiles[:]
        self.normalize = normalize
    def next_frame(self):
        if self.window_size:
            window_size = self.window_size
        else:
            window_size = 1
        sense = random.randint(0,1) if self.type_ is None else self.type_
        if sense:
            _dir = "pos"
            idx = random.randint(0,len(self.posFiles)-1)
            _file = self.posFiles[idx]
        else:
            _dir = "neg"
            idx = random.randint(0,len(self.negFiles)-1)
            _file = self.negFiles[idx]
        cap = cv2.VideoCapture(self.cwd+"/"+_dir+"/"+_file)
        if cap.isOpened():
            num_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            width = self.dim[0] if self.dim[0] else int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = self.dim[0] if self.dim[0] else int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            self.log.log(logger.dbg,"WIDTH: %d \t HEIGHT: %d"%(width,height))
            flag,frame = cap.read()
            if flag:
                num_channels = frame.shape[-1]
            frames = np.empty(shape = [0,height,width,num_channels],dtype = np.float32)
            senses = np.zeros(shape = [window_size],dtype = np.float32)
            cap.set(cv2.CAP_PROP_POS_FRAMES,0)
            pos = random.randint(0,num_frames-window_size-5)
            cap.set(1,pos)
            if self.window_size:
                window_size = self.window_size
            else:
                window_size = 1
            for i in range(window_size):
                flag,frame = cap.read()
                cap.set(1,pos+self.frame_step)
                if flag:
                    frame = cv2.resize(frame,(width,height))
                    frame = self.dtype(frame)
                    if self.normalize:
                        frame = frame/self.dtype(max(frame.flatten()))
                    frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
                    frames = np.append(frames,frame.reshape([1]+list(frame.shape[:])),axis = 0)
                    senses[i] = sense
            self.log.log(logger.dbg,"FRAME SHAPE: {}, Sense Shape: {}".format(frames.shape,senses.shape))
            return frames,senses
        else:
            raise PermissionError("File Not Opened!\n Check the Permissions")
    def __next__(self):
        if self.window_size:
            if self.window_size==1:
                self.log.log(logger.WARN,"Window Size must be more than 1")
                raise ValueError("window size cannot be <=1")

            while True:
                frame,sense = self.next_frame()
                return frame,sense
        else:
            while True:
                frame,sense = self.next_frame()
                return frame[0],sense
