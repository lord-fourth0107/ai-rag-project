
# # I highly do NOT suggest - use Unsloth if possible

# # from peft import AutoPeftModelForCausalLM
# from transformers import AutoTokenizer, AutoModelForCausalLM
# model = AutoModelForCausalLM.from_pretrained(
#     "nsh22/ROS2-Meta-Llama-3.1-8",legacy=False
# )
# tokenizer = AutoTokenizer.from_pretrained("nsh22/tokenizer-ROS2-Meta-Llama-3.1-8")

# import torch

# from transformers import LlamaForCausalLM, LlamaTokenizer

# model_name = "your_huggingface_username/unsloth-llama-finetuned"  # Replace with your model name

# tokenizer = LlamaTokenizer.from_pretrained("nsh22/ROS2-Meta-Llama-3.1-8", legacy=False)

# model = LlamaForCausalLM.from_pretrained("nsh22/ROS2-Meta-Llama-3.1-8", device="cpu", legacy=False) 

# Load model directly
from transformers import AutoModel
model = AutoModel.from_pretrained("Finetuned-LLM")