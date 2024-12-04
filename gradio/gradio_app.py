import gradio as gr
import requests

# Function to process the user's input
def process_question(selected_question):
    url = "https://example.com/api/answer"
    response = requests.post(url, json={"question": question})
    return response.json().get("answer", "Error: No response from backend")
# List of pre-populated questions
questions = [
    "What is AI?",
    "How does Python work?",
    "What is Gradio?"
]

# Gradio interface
with gr.Blocks() as app:
    gr.Markdown("# Pre-Populated Questions App")
    gr.Markdown("### Select a question from the dropdown below to get an answer.")
    
    # Dropdown for questions
    question_input = gr.Dropdown(choices=questions, label="Select a Question", value=questions[0])
    
    # Output display
    output = gr.Textbox(label="Answer", interactive=False)
    
    # Submit button
    submit_btn = gr.Button("Get Answer")
    
    # Event binding
    submit_btn.click(fn=process_question, inputs=question_input, outputs=output)

# Launch the app
app.launch()
