import argparse
import base64
import json
import cv2
import numpy as np
import socketio
import eventlet
import eventlet.wsgi
import time
from PIL import Image
from PIL import ImageOps
from flask import Flask, render_template
from io import BytesIO
import h5py
from keras import __version__ as keras_version
from keras.models import load_model

from keras.models import model_from_json
from keras.preprocessing.image import ImageDataGenerator, array_to_img, img_to_array
#https://www.packtpub.com/mapt/book/application-development/9781785283932/2/ch02lvl1sec26/enhancing-the-contrast-in-an-image
def balance_brightness(image):
	img_yuv = cv2.cvtColor(image, cv2.COLOR_RGB2YUV)
	img_yuv[:,:,0] = cv2.equalizeHist(img_yuv[:,:,0])
	img_out = cv2.cvtColor(img_yuv, cv2.COLOR_YUV2RGB)
	return img_out
# Fix error with Keras and TensorFlow
import tensorflow as tf 

#tf.python_io.control_flow_ops = tf


sio = socketio.Server()
app = Flask(__name__)
model = None
prev_image_array = None

class SimplePIController:
    def __init__(self, Kp, Ki):
        self.Kp = Kp
        self.Ki = Ki
        self.set_point = 0.
        self.error = 0.
        self.integral = 0.

    def set_desired(self, desired):
        self.set_point = desired

    def update(self, measurement):
        # proportional error
        self.error = self.set_point - measurement

        # integral error
        self.integral += self.error

        return self.Kp * self.error + self.Ki * self.integral


controller = SimplePIController(0.1, 0.002)
set_speed = 15
controller.set_desired(set_speed)

@sio.on('telemetry')
def telemetry(sid, data):
    # The current steering angle of the car
    steering_angle = data["steering_angle"]
    # The current throttle of the car
    throttle = data["throttle"]
    # The current speed of the car
    speed = data["speed"]
    # The current image from the center camera of the car
    imgString = data["image"]
    image = Image.open(BytesIO(base64.b64decode(imgString)))
    image_array = np.asarray(image)
    # image_array = balance_brightness(image_array)
    ##image_array = cv2.resize(image_array[60:140,:],(64,64))###my modification
    transformed_image_array = image_array[None, :, :, :]
    # This model currently assumes that the features of the model are just the images. Feel free to change this.
    steering_angle = float(model.predict(transformed_image_array, batch_size=1))

    # The driving model currently just outputs a constant throttle. Feel free to edit this.
    # throttle = 0.32
    # if steering_angle > 0.5:
    # 	throttle = 0.20
    # if 0.15 < steering_angle <= 0.5:
    # 	throttle = 0.25
    # if steering_angle <-0.5:
    # 	throttle = 0.20
    # if -0.5 >= steering_angle > -0.15:
    # 	throttle = 0.25
    throttle = controller.update(float(speed))               ###check
    print(steering_angle, throttle)
    send_control(steering_angle, throttle)                ###check few lines next to this


@sio.on('connect')
def connect(sid, environ):
    print("connect ", sid)
    send_control(0, 0)


def send_control(steering_angle, throttle):
    sio.emit("steer", data={'steering_angle': steering_angle.__str__(),'throttle': throttle.__str__()}, skip_sid=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Remote Driving')
    parser.add_argument('model', type=str, help='Path to model h5 file. Model weights should be on the same path.')
    args = parser.parse_args()
    ##with open(args.model, 'r') as jfile:
        # NOTE: if you saved the file by calling json.dump(model.to_json(), ...)
        # then you will have to call:
        #
        #   model = model_from_json(json.loads(jfile.read()))\
        #
        # instead.
        ##model = model_from_json(jfile.read())
                                                                            ##check the step of using json file to create h5 file
    # check that model Keras version is same as local Keras version
    f = h5py.File(args.model, mode='r')
    model_version = f.attrs.get('keras_version')
    keras_version = str(keras_version).encode('utf8')

    if model_version != keras_version:
        print('You are using Keras version ', keras_version,
              ', but the model was built using ', model_version)

    model = load_model(args.model)
     


    #model.compile("adam", "mse")
    #weights_file = args.model.replace('json', 'h5')
    #model.load_weights(weights_file)

   # if args.image_folder != '':
   #     print("Creating image folder at {}".format(args.image_folder))
   #     if not os.path.exists(args.image_folder):
   #         os.makedirs(args.image_folder)
   #     else:
   #         shutil.rmtree(args.image_folder)
   #         os.makedirs(args.image_folder)
   #     print("RECORDING THIS RUN ...")
   # else:
   #     print("NOT RECORDING THIS RUN ...")

    # wrap Flask application with engineio's middleware
    app = socketio.Middleware(sio, app)

    # deploy as an eventlet WSGI server
    eventlet.wsgi.server(eventlet.listen(('', 4567)), app)
