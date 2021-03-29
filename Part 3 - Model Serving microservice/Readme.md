
### Micro Service
Here we create a micro service for our inference pipeline to use as endpoint. We create a flask API that takes in json input and generates a sentiment score for the input, we will use the model we trained using trainig_pipeline.py to get this job done.
We then dockerize the said API.

#### Run Instructions

1. `docker build -t MicroService:latest .` -- this references the `Dockerfile` at `.` (current directory) to build our Docker image & tags the docker image with `MicroService:latest`

2. Run `docker images` & find the image id of the newly built Docker image

3. `docker run -it --rm -p 5000:5000 {image_id} /bin/bash MicroService/run.sh` -- this refers to the image we built to run a Docker container

If everything worked properly, you should now have a container running, which:

1. Spins up a Flask server that accepts POST requests at http://0.0.0.0:5000/predict

2. Runs a Keras sentiment classifier on the "data" field of the request (which should be a list of text strings: e.g. '{"data": ["this is the best!", "this is the worst!"]}')

3. Returns a response with the model's prediction (1 = positive sentiment, 0 = negative sentiment)

To test this, you can either:

Run `make test_api`

Write your own POST request (e.g. using Postman or curl), here is an example response:

![alt text](https://github.com/siddhant07/CaseStudy2/blob/master/Images/Postman_res.png)

This is how our docker structure looks like:

![alt text](https://github.com/siddhant07/CaseStudy2/blob/master/Images/DockerStructure.png)


For further instructions refer the MakeFile in the MicroService folder.


