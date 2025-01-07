import streamlit as st
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import torch

# Load the pre-trained GPT-2 model and tokenizer from Hugging Face
model_name = "gpt2"  # You can also use "EleutherAI/gpt-neo-125M" for a larger model
model = GPT2LMHeadModel.from_pretrained(model_name)
tokenizer = GPT2Tokenizer.from_pretrained(model_name)

# Function to predict the next words
def predict_next_words(text, num_predictions=5):
    # Encode the input text
    input_ids = tokenizer.encode(text, return_tensors="pt")
    
    # Get the model output for the input text
    with torch.no_grad():
        output = model.generate(input_ids, max_length=len(input_ids[0]) + num_predictions, num_return_sequences=1, no_repeat_ngram_size=2)
    
    # Decode the output back to text
    predicted_text = tokenizer.decode(output[0], skip_special_tokens=True)
    
    # Split the input and predicted text to extract the next words
    predicted_words = predicted_text[len(text):].strip().split()
    
    return predicted_words[:num_predictions]

# Streamlit UI
st.title("Next Word Prediction App")

# Text input
input_text = st.text_input("Enter some text:")

# Display predicted words when the user enters text
if input_text:
    predicted_words = predict_next_words(input_text)
    
    st.write(f"Next words prediction:")
    for i, word in enumerate(predicted_words, 1):
        st.write(f"{i}. {word}")
