# -*- coding: utf-8 -*-
from os import listdir
from os.path import isfile, join
import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import csv
import random
from time import time
from decimal import Decimal
#from faker import Faker
import boto3
import string
import random
import os
import os
import re
import collections
import nltk
import pandas as pd
from flask import jsonify
#from nltk.corpus import stopwords
from io import StringIO # python3; python2: BytesIO 
from nltk.corpus import stopwords
import google.cloud
from google.cloud import language_v1
import os
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('words')

#df_sentimentScore = pd.DataFrame(columns=['sentence','sentiment_score','sentiment_magnitude','language'])
df_sentimentScore = pd.DataFrame(columns=['Text','Label'])
sentiment_score = []
#sentiment_magnitude = []
sentence1 = []
content_list=[]
preprocessed_list=[]
#langue=[]
#stop_words = stopwords.words('english')
s = ""


# Connect to Boto3
s3 = boto3.resource(
    service_name='s3',
    region_name='us-east-2')

# bucket_name = ''
# def upload_to_s3(filename):
#     s3.Bucket(bucket_name).upload_file(Filename=filename, Key='demo/' + filename)
#     print ('Upload Complete')

def upload_to_aws(local_file, bucket, s3_file):
    import boto3
    from botocore.exceptions import NoCredentialsError
    ACCESS_KEY = 'AKIA5CUSOFRV64J75U7W'
    SECRET_KEY = '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'
    s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY,
                      aws_secret_access_key=SECRET_KEY)
    try:
        s3.upload_file(local_file, bucket, s3_file)
        return True
    except FileNotFoundError:
        print("The file was not found")
        return False
    except NoCredentialsError:
        print("Credentials not available")
        return False



 
 #uploading all unstructured files to S3 
def upload_files(path):
    session = boto3.Session(
        aws_access_key_id='AKIA5CUSOFRV64J75U7W',
        aws_secret_access_key='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',
        region_name='us-east-2'
    )
    s3 = session.resource('s3')
    bucket = s3.Bucket('edgarteam3')
 
    for subdir, dirs, files in os.walk(path):
        for file in files:
            full_path = os.path.join(subdir, file)
            with open(full_path, 'rb') as data:
                bucket.put_object(Key=full_path[len(path)+1:], Body=data)
 

def processed_file_to_s3():
    bucket = 'edgarteam3processedfiles' # already created on S3
    csv_buffer = StringIO()

    ACCESS_KEY = 'AKIA5CUSOFRV64J75U7W'
    SECRET_KEY = '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'
   
    df = pd.DataFrame(preprocessed_list)    
    # saving the dataframe  
    df.to_csv('processed.csv')
    df.to_csv(csv_buffer)
    s3_resource = boto3.resource('s3',aws_access_key_id=ACCESS_KEY,
                      aws_secret_access_key=SECRET_KEY)
    s3_resource.Object(bucket, 'processed.csv').put(Body=csv_buffer.getvalue())


def convert_files_to_sent_list():  
    directory = r'/root/EdgarPipeline/call_transcripts'
    #content_list=[]
    #temp_list=[]
    global content_list
    global s
    content = s
    temp_list=content.split(".")
    content_list=content_list+temp_list
    #print("Value of s is"+s)



def remove_emptyrecords():
    while '' in content_list:
        content_list.remove('')
    #print(content_list)



def remove_punctuation():
    for i in content_list:
        re.sub('[^A-Za-z0-9]+', '', i)
    #print(content_list)


def remove_stopwords():
    #preprocessed_list=[]
    for i in content_list: 
        from collections import Counter
        global stop_words
        #stop_words = nltk.download('stopwords')
        stop_words = stopwords.words('english')
        stopwords_dict = Counter(stop_words)
        sent = ' '.join([word for word in i.split() if word not in stopwords_dict])
        preprocessed_list.append(sent)
    #print(preprocessed_list)
    return preprocessed_list
    #print(stopwords_dict)


def analytics_csv():
    import os
    import pandas as pd
    bucket = 'edgarteam3processedfiles'  # already created on S3
    csv_buffer = StringIO()

    ACCESS_KEY = 'AKIA5CUSOFRV64J75U7W'
    SECRET_KEY = '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'
    directory = r'/root/EdgarPipeline/call_transcripts'
    df = pd.DataFrame(columns = ['Company','Revenue','Percent','Comments'])
    c = []
    r = []
    p = []
    co = []
    for filename in os.listdir(directory):
        print(filename)
        temp_list= []
        filepath=r'/root/EdgarPipeline/call_transcripts'+'/'+str(filename)
        #print(filepath)
        f = open(filepath, "r")
        try:
            #with open(r'C:\Users\jaysh\Downloads\sec-edgar\sec-edgar\call_transcripts\AGEN') as f:
            data = f.readlines()
            matching = [s for s in data if "Revenue" in s]
            m2 = [s for s in data if "(" in s]
            m1 = matching[0].split("Revenue",1)[1]
            company = matching[0].split("(",1)[1].split(")",1)[0]
            comments = matching[0].split(')',1)[1].split(' ',1)[1].split('\n',1)[0]
            #print('Revenue is '+ m1.split("$",1)[1].split(' ',1)[0])
            #print('YoY Percentage Change is '+ m1.split('(',1)[1].split(' ',1)[0])
            #print('Company Name '+m2[0].split("(",1)[1].split(")",1)[0])
            matching = [s for s in data if "(" in s]
            company = matching[0].split("(",1)[1].split(")",1)[0]
            revenue = m1.split("$",1)[1].split(' ',1)[0]
            percent = m1.split('(',1)[1].split(' ',1)[0]
            c.append(company)
            r.append(revenue)
            p.append(percent)
            co.append(comments)
            #print(df)
        except:
            print("Revenue and Percentage Change not given")
        f.close()
    df['Company'] = c
    df['Revenue'] = r
    df['Percent'] = p
    df['Comments'] = co
    df.to_csv('/root/EdgarPipeline/Edgar_analytics_csv.csv')
    df.to_csv(csv_buffer)
    s3_resource = boto3.resource('s3', aws_access_key_id=ACCESS_KEY,
                                 aws_secret_access_key=SECRET_KEY)
    s3_resource.Object(bucket, 'Edgar_analytics_csv.csv').put(Body=csv_buffer.getvalue())




# Provide path for service accounts keys for authentication
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"/root/EdgarPipeline/kronosteam4project.json"



def sample_analyze_sentiment(text_content):
    """
    Analyzing Sentiment in a String
    Args:
      text_content The text content to analyze
    """
    #global df_sentimentScore 
    global sentiment_score
    global sentiment_magnitude
    global sentence1
    global langue
    #print(text_content)
    client = language_v1.LanguageServiceClient()
    # text_content = 'I am so happy and joyful.'

    # Available types: PLAIN_TEXT, HTML
    type_ = language_v1.Document.Type.PLAIN_TEXT

    # Optional. If not specified, the language is automatically detected.
    # For list of supported languages:
    # https://cloud.google.com/natural-language/docs/languages
    language = "en"
    document = {"content": text_content, "type_": type_, "language": language}

    # Available values: NONE, UTF8, UTF16, UTF32
    encoding_type = language_v1.EncodingType.UTF8

    response = client.analyze_sentiment(request = {'document': document, 'encoding_type': encoding_type})
    # Get overall sentiment of the input document
    #print(u"Document sentiment score: {}".format(response.document_sentiment.score))


    # Get sentiment for all sentences in the document
    
    for sentence in response.sentences:
        sent = (sentence.text.content)
        sn_score = (sentence.sentiment.score)
        #sn_magnitude = (sentence.sentiment.magnitude)
        #language1 = (response.language)
        if len(sent) > 30:
            sentence1.append(sent)
            sentiment_score.append(sn_score)



# [END language_sentiment_text]


def sentiment_main(passed_list):
    #import argparse

    #parser = argparse.ArgumentParser()
    #parser.add_argument("--text_content", type=str, default=["I am so happy and joyful.","Ifyou are bad I'm your dada"])
    #args = parser.parse_args()
    #label_list=["I am so happy and joyful.","Ifyou are bad I'm your dada","I am so happy and joyful.","Ifyou are bad I'm your dada"]
    #remove_stopwords()
    #processed_list=processed_list[0:5]
    count = 0
    for i in passed_list:
        #print(i)
        sample_analyze_sentiment(i)
        count = count + 1
        if count == 30:
            break
        
            


# if __name__ == "__main__":
#     #print("main")
#     upload_files('call_transcripts')
#     print("file uploaded successfully to s3")
#     convert_files_to_sent_list()
#     remove_emptyrecords()
#     remove_punctuation()
#     preprocessed_list=remove_stopwords()
#     print("Preprocessing done")
#     processed_file_to_s3()
#     print("preprocessed files in s3")
#     analytics_csv()
#     print("analytics generated")
#     sentiment_main(preprocessed_list)
#     print("data labebelled using Google API")
#     store_data_to_dataframe()
#     print("CSV generated")
#     print(sentence1)
#     print(sentiment_score)
#     #print(sentiment_magnitude)
#     #print(langue)

#sent_text = Scrape()
#IBMSentimentAnalysis()


#################### FAST API PART ###############################33

app = FastAPI()

# Specify your Data Directory here
data_dir = './inference-data/'
companies = [f for f in listdir(data_dir) if isfile(join(data_dir, f))]


class Item(BaseModel):
    company: str
    year: int


@app.get("/call-transcripts/{company}/{year}")
def get_data(company: str, year: int):

    global s
    bucket = 'edgarteam3processedfiles' # already created on S3
    csv_buffer = StringIO()

    ACCESS_KEY = 'AKIA5CUSOFRV64J75U7W'
    SECRET_KEY = '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'
    if company in companies and year == 2021:
        with open(data_dir + company) as f:
            s = f.read()

            convert_files_to_sent_list()
            remove_emptyrecords()
            remove_punctuation()
            preprocessed_list=remove_stopwords()
            sentiment_main(preprocessed_list)
            
            print("CSV generated")
            print(sentence1)
            print(sentiment_score)
            print(type(sentiment_score))
            for i in range(len(sentiment_score)):
                if sentiment_score[i] >= 0.1:
                    sentiment_score[i] = "Positive"
                else:
                    sentiment_score[i] = "Negative"

            # Creating a CSV Fie
            df_sentimentScore['Text'] = sentence1
            df_sentimentScore['Label'] = sentiment_score
            df_sentimentScore.to_csv('/root/Inference Part/transcript-simulated-api/Sentiment_Labled_Data_csv.csv')

            # Uploading Files to Amazon S3
            df_sentimentScore.to_csv(csv_buffer)
            s3_resource = boto3.resource('s3', aws_access_key_id=ACCESS_KEY,aws_secret_access_key=SECRET_KEY)
            s3_resource.Object(bucket, 'Sentiment_Labled_Data_from_FASTAPI.csv').put(Body=csv_buffer.getvalue())

        return {"Sentence": sentence1, "Predict": sentiment_score}
        
    else:
        raise HTTPException(status_code=404, detail="Company not found")


if __name__ == '__main__':
    uvicorn.run(app, port=8080, host='0.0.0.0')