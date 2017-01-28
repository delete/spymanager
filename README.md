# Spy Manager bot

Create and manager groups of users from ImageSite getting the latest (12 till now) posted photos from each user.


## Environment file

Create a `.env` file on the project root folder:

```sh
API_TOKEN=MY_TELEGRAM_API
ADMIN_ID=YOUR_ID
```

## Run

`docker-compose build && docker-compose up`

## Code example without bot:

### Install dependencies

`pip install -r requeriments.txt`

### Applictaion

**MongoDB Server**

To store the data into a separated container:

`docker volume create --name mongodata`

Runing:

`docker run -d -p 27017:27017 --name mongod -v mongodata:/data mongo mongod`

`python example.py`