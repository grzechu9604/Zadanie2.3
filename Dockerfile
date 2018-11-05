FROM ubuntu:latest

# Install latest updates
RUN apt-get update
RUN apt-get upgrade -y

# Install your software
RUN DEBIAN_FRONTEND=noninteractive apt-get -y install sqlite3
RUN DEBIAN_FRONTEND=noninteractive apt-get -y install python3
#RUN DEBIAN_FRONTEND=noninteractive apt-get -y install python3-pip
#RUN DEBIAN_FRONTEND=noninteractive pip3 install -y datetime
#RUN DEBIAN_FRONTEND=noninteractive pip3 install -y sqlite3

# Set working dir
WORKDIR .

# Copy dataset to working dir
COPY unique_tracks.txt .
COPY triplets_sample_20p.txt .

# Copy your code
COPY main.py .

# Set starting command (run your code)
CMD python3 main.py