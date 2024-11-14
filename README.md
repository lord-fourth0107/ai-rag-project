# AI- Project : RAG Implementation

## Infrastructure setup for Mac OS 
### Prerequisites
1. Docker Setup
2. Docker is up and running
3. No conflicting daemon is running 

## Setting up MongoDB

Pull the latest docker image of MongoDB using the cmd:

```
docker run --name mongodb -p 27017:27017 -d mongodb/mongodb-community-server:5.0-ubuntu2004
```
Run the image by running the below command

```
docker run --name mongodb -p 27017:27017 -d mongodb/mongodb-community-server:latest
```

This starts a container of mongodb at localhost:27017


