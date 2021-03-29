from __future__ import absolute_import, division, print_function, unicode_literals

import numpy as np

import tensorflow as tf

#pip install tensorflow-hub
#pip install tfds-nightly
import tensorflow_hub as hub
#import tensorflow_datasets as tfds

print("Version: ", tf.__version__)
print("Eager mode: ", tf.executing_eagerly())
print("Hub version: ", hub.__version__)
print("GPU is", "available" if tf.config.experimental.list_physical_devices("GPU") else "NOT AVAILABLE")

import pandas as pd
from io import StringIO
import boto3
from botocore.exceptions import NoCredentialsError
import pandas as pd
import io
import re
import csv

def run_pipeline():
	ACCESS_KEY = 'AKIA5CUSOFRV64J75U7W'
	SECRET_KEY = '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'
	s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY,
                      aws_secret_access_key=SECRET_KEY)
	csv_obj = s3.get_object(Bucket= 'edgarteam3labeldata', Key= 'Sentiment_Labled_Data_csv.csv')
	body = csv_obj['Body']
	csv_string = body.read().decode('utf-8')
#
	df = pd.read_csv(StringIO(csv_string))
	df['label'] = pd.Categorical(df['label'])
	df['label'] = df.label.cat.codes

	train_dataset=(
		tf.data.Dataset.from_tensor_slices(
			(
				df['text'],
				df['label']
			)
		)
	)
	
	embedding = "https://tfhub.dev/google/tf2-preview/nnlm-en-dim128/1"
	hub_layer = hub.KerasLayer(embedding, input_shape=[], 
                           dtype=tf.string, trainable=True)
						 
	model = tf.keras.Sequential()
	model.add(hub_layer)
	model.add(tf.keras.layers.Dense(16, activation='relu'))
	model.add(tf.keras.layers.Dense(1))
	
	model.compile(optimizer='adam',
              loss=tf.keras.losses.BinaryCrossentropy(from_logits=True),
              metrics=['accuracy'])
	
	model.fit(train_dataset.shuffle(2000).batch(512),
                    epochs=30)
					
	model.save("my_model.h5")
	with open("my_model.h5", "rb") as f:
		s3.upload_fileobj(f, "edgarteam3model", "model_h5")
	return


if __name__ == "__main__":
	run_pipeline()
