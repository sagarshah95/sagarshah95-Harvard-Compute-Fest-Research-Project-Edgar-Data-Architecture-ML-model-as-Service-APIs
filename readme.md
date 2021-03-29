## ML Pipeline to train and deploy sentiment analysis model as a service
In this assignment, We have build a sentiment analysis micro service that could take a new Edgarfile in json format and generate sentiments for each statement in the referenced EDGAR file.

To build this service, we need a Sentiment analysis model that has been trained on “labeled”,“Edgar” datasets. 

Note that you need to have labeled data which means someone has to label thestatements and you need to use EDGAR datasets since we want the ML service to be optimizedfor domain-specific datasets.

In order to accomplish this, we have designed 3 pipelines. ​We have used Airflow pipelining tools to define our pipelines.

## Report

https://codelabs-preview.appspot.com/?file_id=1hUkyf5xo1fJJzFPbH9cUKZ2AtX83ExkLmnQc7rYuwZ8#0

## Prerequisites - What  do we need 
Things you need to install:
(note: if you can simply load docker file from docker hub, its containerized app)

Python3.5+\
AWS S3\
Google understanding api 
https://cloud.google.com/natural-language/docs/sentiment-tutorial \
Docker\
Postman\
Apache Airflow 


## Prerequisites - Steps
Your development and production environments are constructed by [Docker](docker.com). Install Docker for Desktop for your OS.

To verify that Docker is installed, run `docker --version`.

## Setup your Container
In this directory, we have `Dockerfile`, a blueprint for our development environment, and `requirements.txt` that lists the python dependencies.

To serve the provided pre-trained model, follow these steps:
1. `git clone` this repo
2. `cd ./assignment2`
3. `docker build -t assignment2.` -- this references the `Dockerfile` at `.` (current directory) to build our **Docker image** & tags the docker image with `akashmdubey/assignment2:latest`
4. Run `docker images` & find the image id of the newly built Docker image, OR run `docker images | grep ml_deploy_demo | awk '{print $3}'`
5. `docker run -it --rm -p 5000:5000 {image_id} /bin/bash ml/run.sh` -- this refers to the image we built to run a **Docker container**

If everything worked properly, you should now have a container running, which:

1. Spins up a Flask server that accepts POST requests at http://0.0.0.0:5000/predict

2. Runs a customized Keras sentiment classifier on the `"data"` field of the request (which should be a **list of text strings**: e.g. `'{"data": ["this is the best!", "this is the worst!"]}'`)

3. Returns a response with the model's prediction ( positive sentiment, negative sentiment)

To test this, you can either:
1. Create custom `test_api`
2. Write your own POST request (e.g. using [Postman](https://www.getpostman.com/) or `curl`), here is an example response:
```

INPUT : 
{
  "Sentence": [
    "(NKE) CEO John Donahoe Q3 2021 Results - Earnings Call Transcript Mar",
    "(NKE) Q3: 2021-03-18 Earnings Summary EPS $0",
    "(NYSE:NKE) Q3 2021 Earnings Conference Call March 18, 2021 5:00 PM ET Company Participants Andy Muir - Vice President, Investor Relations John Donahoe - President Chief Executive Officer Matt Friend - Chief Financial Officer Conference Call Participants Bob Drbul - Guggenheim Securities Michael Binetti - Credit Suisse Erinn Murphy - Piper Sandler Omar Saad - Evercore ISI Jamie Merriman - Bernstein Operator Good afternoon, everyone welcome NIKE, Inc",
    "Fiscal 2021 Third Quarter Conference Call was really good"
  ],
  "Predict": [
    "Positive",
    "Negative",
    "Negative",
    "Positive",
    "Positive"
  ]
}
```


## Project Structure
```
Folder PATH listing for volume OS
Volume serial number is B444-80E3
C:.
|   Dockerfile
|   output.doc
|   readme.md
|   requirements.txt
|   run.sh
|   
+---Images
|       Gantt_View_of_Annotation_Pipeline.png
|       Graph_View_of_Annotation_Pipeline.png
|       Graph_View_of_Main_Pipeline.png
|       Graph_View_of_Training_Pipeline.png
|       Tree_View_of_Annotation_Pipeline.png
|       Tree_View_of_Main_Pipeline.png
|       Tree_View_of_Training_Pipeline.png
|       
+---Part 1 - Annotation Pipeline
|   |   Edgar_analytics_csv.csv
|   |   kronosteam4project.json
|   |   Sentiment_Labled_Data_csv.csv
|   |   
|   +---call_transcripts
|   |       AGEN.txt
|   |       ALTG.txt
|   |       AXU.txt
|   |       
|   \---dags
|           EdgarAnnotation.py
|           Establish_Connection_With_Google_API.py
|           Generating_Analytics_Files.py
|           jayshil_dag.py
|           Preprocess_The_Data.py
|           processing.py
|           test.py
|           Upload_Raw_Data_to_AWS_S3.py
|           Upload_to_AWS_S3.py
|           
+---Part 2 - Training Pipeline
|   |   .gitignore
|   |   keras_final.py
|   |   Readme.md
|   |   unittests.cfg
|   |   
|   \---dags
|           main_airflow.py
|           training.py
|           
+---Part 3 - Model Serving microservice
|   |   Readme.md
|   |   requirements.txt
|   |   
|   \---team3-edgar-server
|       \---app
|           |   app.py
|           |   main.css
|           |   __init__.py
|           |   
|           +---static
|           |   \---css
|           |           styles.css
|           |           
|           +---templates
|           |       base.html
|           |       files.html
|           |       index.html
|           |       layout.html
|           |       
|           \---__pycache__
|                   app.cpython-38.pyc
|                   app1.cpython-38.pyc
|                   __init__.cpython-38.pyc
|                   
\---Part 4 - Inference Pipeline
    |   Readme.md
    |   
    \---transcript-simulated-api
        |   inference.py
        |   main.py
        |   Sentiment_Labled_Data_csv.csv
        |   
        \---inference-data
                ACFN
                AGEN
                ALTG
                AXU
 

```
## Architecture:

![](https://github.com/jayshilj/Team3_CSYE7245_Spring2021/blob/main/Assignments/Assignment%202/Images/Edgararchitecture.jpg)


## Setup For Running this Project:

#### Step 0: Clone Project, Setup Airflow
Clone this repo and edit the code with your AWS Credentials, Google Credentials and your s3 bucket path and then setup the Apache Airflow


#### Step 1 : Part 1 Annotation Pipeline
Run the annotation pipeline in Apache Airflow, you will have the processed files & label files using Google APIs saved in your bucket.

![](https://github.com/jayshilj/Team3_CSYE7245_Spring2021/blob/main/Assignments/Assignment%202/Images/AnnotationDiagram.jpg)

![](https://github.com/jayshilj/Team3_CSYE7245_Spring2021/blob/main/Assignments/Assignment%202/Images/Graph_View_of_Annotation_Pipeline.png)


#### Step 2 : Part 2 Training Pipeline
Run the training pipeline in Apache Airflow, you will have the h5 model saved in your bucket.

![](https://github.com/jayshilj/Team3_CSYE7245_Spring2021/blob/main/Assignments/Assignment%202/Images/Graph_View_of_Annotation_Pipeline.png)

##### TensorBoard Observations - Accuracy Increases, Loss Decreases
![](https://github.com/jayshilj/Team3_CSYE7245_Spring2021/blob/main/Assignments/Assignment%202/Images/TensorBoard.png)

![](https://github.com/jayshilj/Team3_CSYE7245_Spring2021/blob/main/Assignments/Assignment%202/Images/TrainingPipeline.jpg)


#### Airflow Main Combing Annotation and Training Pipeline

![](https://github.com/jayshilj/Team3_CSYE7245_Spring2021/blob/main/Assignments/Assignment%202/Images/Graph_View_of_Main_Pipeline.png)

![](https://github.com/jayshilj/Team3_CSYE7245_Spring2021/blob/main/Assignments/Assignment%202/Images/Tree_View_of_Main_Pipeline.png)

![](https://github.com/jayshilj/Team3_CSYE7245_Spring2021/blob/main/Assignments/Assignment%202/Images/Gantt_View_of_Annotation_Pipeline.png)

#### Step 3 : Part 3: Microservices

![](https://github.com/jayshilj/Team3_CSYE7245_Spring2021/blob/main/Assignments/Assignment%202/Images/MicroService.jpg)

Successful Built of Docker Image:

![](https://github.com/jayshilj/Team3_CSYE7245_Spring2021/blob/main/Assignments/Assignment%202/Images/DockerVscode.jpg)

![](https://github.com/jayshilj/Team3_CSYE7245_Spring2021/blob/main/Assignments/Assignment%202/Images/DockerHomeImages.jpg)

![](https://github.com/jayshilj/Team3_CSYE7245_Spring2021/blob/main/Assignments/Assignment%202/Images/dockerimagevscode.jpg)



Build a Docker Image, create a Docker Container and run the container. If everything is working properly, you should be able to send HTTP POST requests to http://localhost:5000/predict and get results back from the model!

#### Step 4 : Part 4: Inference Pipeline
Once  everything is working properly, We will use Inference APIs to call flat files and do preprocessing on files and sent it against built http://localhost:5000/predict and get results back from the model !


![](https://github.com/jayshilj/Team3_CSYE7245_Spring2021/blob/main/Assignments/Assignment%202/Images/InferencePipeline.jpg)

![](https://github.com/jayshilj/Team3_CSYE7245_Spring2021/blob/main/Assignments/Assignment%202/Images/dockercontainer.jpg)

![](https://github.com/jayshilj/Team3_CSYE7245_Spring2021/blob/main/Assignments/Assignment%202/Images/DockerFinalsuccess.jpg)

![](https://github.com/jayshilj/Team3_CSYE7245_Spring2021/blob/main/Assignments/Assignment%202/Images/Dockerisedapprespondingrequests.jpg)

![](https://github.com/jayshilj/Team3_CSYE7245_Spring2021/blob/main/Assignments/Assignment%202/Images/FastAPI_Output.png)


#### Step 5 : Analytics from the EDGAR Dataset

![](https://github.com/jayshilj/Team3_CSYE7245_Spring2021/blob/main/Assignments/Assignment%202/Images/AnalyticsCSV.png)

![](https://github.com/jayshilj/Team3_CSYE7245_Spring2021/blob/main/Assignments/Assignment%202/Images/Visualization_Edgar.png)



You can test this using Postman.

## Authors 
<b>[Akash M Dubey](https://www.linkedin.com/in/akashmdubey/)</b> 

<b>[Jayshil Jain](https://www.linkedin.com/in/jayshiljain/)</b> 

<b>[Sagar Shah](https://www.linkedin.com/in/shahsagar95/)</b> 
