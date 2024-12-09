# AI Finetuned RAG System CS-GY-6613

Submitted By: 
| Sl.N0 | Name                 | Net ID  |
| ----  |:--------------------:| -------:|
| 1     | Uttam Singh          |  us2193 |
| 2     |   Namani Shreeharsh  |  sn4165 |


Platform Used for Docker Desktop: MAC OS

Docker images are platform independent but not the daemon . Hence to have compatibity for clearml we have noted few steps to run the RAG projects

## Steps to run the RAG model on ROS.
- 1. Docker Desktop or docker daemon should be installed 
### Step1 Prerequisites:

Follow the steps from 1 to 11 in the below link to create clearml related services (docker services such as clearml-fileserver, clearml-apiserver, clearml-webserver) this will result in a clearml specific docker compose file., which should be like clearml-compose.yml file in the final-instruct-db branch

```
https://clear.ml/docs/latest/docs/deploying_clearml/clearml_server_linux_mac/

```

## Step2: 
run the below command to launch all the required docker services and images, in the project directory:
```
docker compose -f /opt/clearml/docker-compose.yml -f docker-compose.yml up -d
```

## Step3: 
run a command inside the ollama image launched from the above docker compose to run the finetuned model, which is pushed to huggingface

Ollama provides good orchestration and library to pull multiple models from huggingface or opensource . This is one of the reason we went with ollama docker image to run the finetuned model. This inherently decouples the model with code. So we can now push any changes to model and code independently of each other

```
docker exec -it ollama_container ollama run hf.co/nsh22/ROS-gguf
```
This sets up the RAG model and code to run together and the gradio app can be launched  in browser
## Submission of the project:

### Docker Compose 

![image](https://github.com/user-attachments/assets/311fb142-2de2-4c6a-b65f-485d8e19498d)

### Gradio app results

The below submission contains the screenshots of the question and answers in Gradio application:

<img width="1430" alt="Screenshot 2024-12-08 at 13 45 10" src="https://github.com/user-attachments/assets/74fc4a2f-d7be-49f7-a2f5-351cdad1df07">
<img width="1226" alt="Screenshot 2024-12-08 at 13 44 53" src="https://github.com/user-attachments/assets/265fdf8d-23b6-4d22-b4a0-daea27100e86">
<img width="1251" alt="Screenshot 2024-12-08 at 13 41 37" src="https://github.com/user-attachments/assets/b49ef9d5-9d20-4bc3-9368-ebd551a66144">

## Without context result of LLM

<img width="1440" alt="Screenshot 2024-12-08 at 8 12 26 PM" src="https://github.com/user-attachments/assets/067d41de-8729-48be-875e-2543dfad601d">

Difference: With Context enhanced prompt the response generated is more latest as it contains instructions for wide range of OS while without context we have response only for Ubuntu for which ROS was first developed
---------------------------------------------------------------------------------------------------------------------------------------
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
