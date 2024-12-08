import gradio as gr
import requests

# Define the backend URL
BACKEND_URL = "http://127.0.0.1:5303/getAnswer"  

# Prepopulated questions
# The `QUESTIONS` list in the code snippet provided is prepopulating the questions that the user can
# select from a dropdown menu in the Gradio interface. These questions will be used as input to the
# backend API when the user selects one and clicks the "Get Answer" button. The selected question will
# be sent to the backend URL for processing, and the response will be displayed in the output textbox
# on the interface. This setup allows users to easily select a question of interest and receive an
# answer from the backend service.
QUESTIONS = [
    "What is ROS?",
    "Steps to install ROS?",
    "What is the latest version of ROS?",
    "Tell me how can I navigate to a specific pose - include replanning aspects in your answer.",
    "Give me some getting started  code for ROS2 in python?"
]

# Function to send a request to the backend
def fetch_answer(question):
    """
    The `fetch_answer` function sends a POST request to a backend API with a question, retrieves the
    response, and handles any request exceptions.
    
    :param question: The `fetch_answer` function takes a question as input, makes a POST request to a
    backend URL with the question as a JSON payload, and returns the response from the backend. If an
    error occurs during the request, it will return an error message
    :return: The fetch_answer function takes a question as input, makes a POST request to a backend URL
    with the question as a JSON payload, and then returns the response from the backend. If the request
    is successful, it returns the response from the backend. If there is an error during the request, it
    returns an error message indicating the issue. If no answer is provided by the backend, it returns
    "No
    """
    try:
        # Make a POST request to the backend
        response = requests.post(BACKEND_URL, json={"query": question})
        response.raise_for_status()
        return response.json().get("response", "No answer provided by the backend.")
    except requests.exceptions.RequestException as e:
        return f"Error fetching the response: {e}"




def pre_launch():
    """
    The `pre_launch` function sets up a Question Answering App interface with a dropdown for selecting
    questions, a button to fetch answers, and a textbox to display the response.
    """
  

    with gr.Blocks() as applet:
            pass
            gr.Markdown("# Question Answering App")
            gr.Markdown("Select a question from the dropdown below and get an answer from the backend.")

            with gr.Row():
                question_dropdown = gr.Dropdown(QUESTIONS, label="Select a Question")
                submit_button = gr.Button("Get Answer")

            output_text = gr.Textbox(label="Response", lines=5, interactive=False)

            submit_button.click(fetch_answer, inputs=question_dropdown, outputs=output_text)
    applet.launch()


def launch_gradio_app():
    """
    The function `launch_gradio_app` is defined in Python and calls the `pre_launch` function before
    launching the Gradio app.
    """
    pre_launch()