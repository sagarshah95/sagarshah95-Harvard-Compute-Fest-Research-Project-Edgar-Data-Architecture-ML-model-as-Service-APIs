#Team 3 Author : Akash Jayshil Sagar
# we start with tensorflow docker image
#note for faster run we do base image pull from docker hub 

ARG BASE_IMG=tokunagaken/tensorflow-keras-jupyter-py3
FROM $BASE_IMG

#docker pull tokunagaken/tensorflow-keras-jupyter-py3
#Use working directory /app
WORKDIR /

#Copy all the content of current directory to /app
ADD . /

# pip3 by default as the base image is python
RUN pip install --upgrade pip setuptools wheel && \
    pip install -r requirements.txt

# set the default user
# USER $Team_3

ENTRYPOINT [ "python" ]

CMD [ "./bdia-server/app/app.py" ]