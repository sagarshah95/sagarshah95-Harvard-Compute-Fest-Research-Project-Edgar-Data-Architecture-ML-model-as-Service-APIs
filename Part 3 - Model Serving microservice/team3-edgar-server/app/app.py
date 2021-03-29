from flask import Flask, request, jsonify, abort
import boto3
import tensorflow as tf
import json
from keras.models import load_model
import h5py
import tensorflow_hub as hub
import keras
from flask import Flask, request, jsonify, render_template
import numpy as np
from tensorflow.keras import backend
from tensorflow.keras.models import load_model

#load model from dockerized folder via container for faster load

model = tf.keras.models.load_model(r'./Training_pipeline/my_model.h5',
                                            custom_objects={'KerasLayer': hub.KerasLayer}, compile=True)


app = Flask(__name__)

#removing S3 keys for protection - AMD - AWS 
#once downloaded 1.8GB model- have dockerized it to make it faster 

# BUCKET_NAME = 'edgarteam3model'
# KEY = 'model_h5'
# ACCESS_KEY = ''
# SECRET_KEY = ''

# s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY)
# s3.Bucket(BUCKET_NAME).download_file(KEY, 'my_model.h5')

@app.route('/predict', methods=['POST'])
def index():
    body_dict = request.get_json(silent=True)
    data = body_dict['data']

    prediction = predictonline(data)

    result = {'prediction': prediction}
    return json.dumps(result)

def predictonline(data):
    global model
    return model.predict(data).tolist()

def main():
    """Run the app."""
    app.run(host='0.0.0.0', port=8888, debug=False) 

if __name__ == '__main__':
    main()