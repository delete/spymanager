# Spy Manger bot

Create and manager groups of users from ImageSite getting the latest (12 till now) posted photos from each user.


## Install

`pip install -r requeriments.txt`


## Run

`docker-compose build && docker-compose up`


## Code example without bot:

**MongoDB Server**

To store the data into a separated container:

`docker volume create --name mongodata`

Runing:

`docker run -d -p 27017:27017 --name mongod -v mongodata:/data mongo mongod`

`python example.py`