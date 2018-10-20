import tensorflow as tf
from keras.models import Model,Sequential
from keras.callbacks import ModelCheckpoint
from keras.layers import Conv2D,MaxPooling2D,LeakyReLU,Flatten,TimeDistributed,CuDNNLSTM,Input,Dense,GlobalAveragePooling2D,Reshape,Dropout,BatchNormalization
from keras.applications.resnet50 import ResNet50
LSTM = CuDNNLSTM
import numpy as np
from frames import FrameData
import matplotlib.pyplot as plt
frames = 10
fd1 = FrameData(".",dim = (320,320))
fd2 = FrameData(".",dim = (320,320))
width = 320
height = 320
channels = 3
def build_model():
  I = Input(shape = [frames,width,height,channels])
  #cnn = ResNet50(input_shape = (width,height,channels),include_top = False,weights = "imagenet")
  i = Input(shape = (width,height,channels))
  cnn = Conv2D(512,kernel_size = 5,strides = [2,2])(i)
  cnn = MaxPooling2D(5,strides = [2,2])(i)
  cnn = BatchNormalization()(cnn)
  cnn = LeakyReLU(0.2)(cnn)
  cnn = Conv2D(128,kernel_size = 5,strides = [2,2])(cnn)
  cnn = MaxPooling2D(5,strides = [2,2])(cnn)
  cnn = BatchNormalization()(cnn)
  cnn = LeakyReLU(0.2)(cnn)
  cnn = Conv2D(32,kernel_size = 5,strides = [2,2])(cnn)
  cnn = MaxPooling2D(5,strides = [2,2])(cnn)
  cnn = BatchNormalization()(cnn)
  cnn = LeakyReLU(0.2)(cnn)
  #print(resnet.output_shape)
  #cnn.trainable = False
  #cnn.summary()
  cnn = Flatten()(cnn)
  cnn = Dense(32)(cnn)
  cnn = Dense(2,activation = "softmax")(cnn)
  model = Model(inputs = [i],outputs = [cnn])
  return model
  
#es = .f.keras.callbacks.EarlyStopping('loss',patience = 1,min_delta = 0)
#model =. build_model()
model = build_model()
model.compile(optimizer = tf.train.AdamOptimizer(learning_rate = 0.0001),loss = tf.keras.losses.binary_crossentropy)
def gen(fd,batch_size = 2):
  fs = []
  ss = []
  bs = 1
  while True:
    frame,sense = next(fd)
    if bs%batch_size != 0:
      fs.append(frame)
      ss.append(sense[0])
      bs+=1
    else:
      yield np.array(fs),np.array(ss)#.reshape(batch_size-bs-1,1)
ckpt = ModelCheckpoint(filepath = "cnn-lstm.h5",save_best_only = True,verbose = 1)
model.fit_generator(gen(fd1,batch_size = 64),steps_per_epoch = 100,epochs = 6,callbacks = [ckpt])
def predict(vid):
	assert window_size ==frames:
	f= frame.reshape([1]+list(frame.shape[:]))
	v = model.predict(f)
	return v[0]
