# sudo docker build -t reecepbcups/commonwealth_notification_website .
# sudo docker run -p 8080:8080 reecepbcups/commonwealth_notification_website
#
# sudo docker login
# sudo docker push reecepbcups/commonwealth_notification_website

# start by pulling the python image
FROM python:3.8-alpine

# copy the requirements file into the image
COPY ./requirements.txt /app/requirements.txt

COPY ./chains.json /app/chains.json
COPY ./config.json /app/config.json

# switch working directory
WORKDIR /app

# install the dependencies and packages in the requirements file
RUN pip install -r requirements.txt

# copy every content from the local file to the image
COPY . /app

# configure the container to run in an executed manner
ENTRYPOINT [ "python" ]

CMD ["website.py" ]