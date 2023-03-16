# Ordering Portal
A ordering portal for ordering radiology images for research purposes. This webb app is a full-stack flask application.

# Run locally
## Installation
`pip install -r requirements.txt`

## Run the application
`cd ordering_portal`

`flask run`

# Run in docker

## Build image
`docker build --tag ordering_portal .`

## Run container
The best solution is to run the image in detached mode. Because we need to view this application in the browser rather than the container, we'll modify our docker run and add two additional tags: "-d" to run it in detached mode and "-p" to specify the port to be exposed. 

`docker run -d -p 5000:5000 ordering_portal`

### or

## Pull image
`docker pull gustavlagneborg/ordering_portal`
## Run container
The best solution is to run the image in detached mode. Because we need to view this application in the browser rather than the container, we'll modify our docker run and add two additional tags: "-d" to run it in detached mode and "-p" to specify the port to be exposed. 

`docker run -d -p 5000:5000 gustavlagneborg/ordering_portal`

## Access 
For local access visit: 127.0.0.1:5000/

