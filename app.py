from flask import Flask, redirect, url_for, request, render_template
from werkzeug.utils import secure_filename

import tensorflow as tf

from tensorflow.keras.preprocessing import image



import matplotlib.pyplot as plt
import matplotlib.image as mpimg


import pathlib
import os
import random




UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'static', 'uploads')

MODEL_PATH = 'cotton_cnn.h5'


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


model = tf.keras.models.load_model(MODEL_PATH)

@app.route('/')
@app.route('/home')
def index():
    return render_template('index.html')




def predict_image(model,file_path):
    
    img = tf.io.read_file(file_path)
    image = tf.image.decode_image(img)
    
    image = tf.image.resize(image, size = (224,224))
    image = image / 255.

    class_name = ['fresh cotton leaf' , 'fresh cotton leaf']
   
    predict = model.predict(tf.expand_dims(image, axis=0))
    print(tf.round(predict))
    predict_class = class_name[int(tf.round(predict))]
   
    print(f'prediction : {predict_class}')
    
    return predict


@app.route('/predict', methods = ['GET', 'POST'])
def prediction():
    
    if request.method == 'POST':
        # Get the file from post request
        print(request.files, request.form, request.args)
        f = None
        if 'image' in request.files: f = request.files['image']
        if f:
            # Save the file to ./uploads
            file_path = os.path.join(
                app.config['UPLOAD_FOLDER'], secure_filename(f.filename))
            f.save(file_path)
            
            
            class_name = ['Diseased cotton leaf' , 'fresh cotton leaf']
            predict = predict_image(model, file_path)
            predict_class = class_name[int(tf.round(predict))]
            result = predict_class
            return render_template('predict.html', result = result, img = secure_filename(f.filename) )
        return render_template('predict.html', result = None, err = 'failed to receive file')
    return render_template('predict.html', result = None)


if __name__ == ("__main__"):
    app.run(debug=True)
    

@app.route('/performance')
def model_performance():
    return render_template('performance.html')