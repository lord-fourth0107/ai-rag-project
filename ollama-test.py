import ollama

ros_prompt = """Below is an instruction that asks a question related to ROS. Write a response that appropriately completes the request.

### Instruction:
{}


### Response:
{}"""
ros_prompt.format(
        "Explain code structure of ROS2?", # instruction
        "",
    )
response = ollama.chat(model = "hf.co/nsh22/ROS-gguf", messages=[{'role':'user','content':ros_prompt}])
print(response['message']['content'])