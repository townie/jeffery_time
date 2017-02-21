FROM kavolorn/opencv

# setup up requirements
RUN apt-get update && apt-get -yqq install python3-pip
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

# get data
COPY . /data
WORKDIR data

# run server
EXPOSE 5222
CMD python3 server.py