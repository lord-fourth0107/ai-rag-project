# ROS Helper

## How to check for data in mongoDB

### Prerequisites mogosh installed
Run command on terminal
```
mongosh --port 27017
```

Run the below commands in steps 

```
show dbs
```
```
use rag
```
```
show collections
```
```
db.repositories.find()
```


# Steps to run the RAG model on ROS.

## Step1:
Follow the steps from 1 to 11 in the below link to create clearml related services (docker services such as clearml-fileserver, clearml-apiserver, clearml-webserver) this will result in a clearml specific docker compose file., which should be like clearml-compose.yml file in the final-instruct-db branch

## Step2: 
run the below command to launch all the required docker services and images, in the project directory:
```
docker compose -f /opt/clearml/docker-compose.yml -f docker-compose.yml up -d
```

## Step3: 
run a command inside the ollama image launched from the above docker compose to basically run the finetuned model, which we finetuned and pushed to huggingface

```
docker exec -it ollama_container ollama run hf.co/nsh22/ROS-gguf
```

## Step4: 
run app.py file to begin the flask server and gradio app
```
    Python app.py
```
Submission of the project:

The below submission contains the screenshots of the question and answers in Gradio application:
