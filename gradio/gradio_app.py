import gradio as gr
import requests

# Define the backend URL
BACKEND_URL = "http://127.0.0.1:5000/getAnswer"  

# Prepopulated questions
QUESTIONS = [
    "What is ROS?",
    "Steps to install ROS?",
    "What is the latest version of ROS?",
    "Tell me how can I navigate to a specific pose - include replanning aspects in your answer.",
    "What are the benefits of cloud computing?"
]

# Function to send a request to the backend
def fetch_answer(question):
    try:
        # Make a POST request to the backend
        response = requests.post(BACKEND_URL, json={"query": question})
        response.raise_for_status()
        return response.json().get("response", "No answer provided by the backend.")
    except requests.exceptions.RequestException as e:
        return f"Error fetching the response: {e}"

# Build the Gradio interface
with gr.Blocks() as app:
    gr.Markdown("# Question Answering App")
    gr.Markdown("Select a question from the dropdown below and get an answer from the backend.")

    with gr.Row():
        question_dropdown = gr.Dropdown(QUESTIONS, label="Select a Question")
        submit_button = gr.Button("Get Answer")

    output_text = gr.Textbox(label="Response", lines=5, interactive=False)

    submit_button.click(fetch_answer, inputs=question_dropdown, outputs=output_text)

# Launch the app
app.launch()
