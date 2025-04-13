import streamlit as st
import random
import time
import requests
import json
from flask import Flask, request
import google.generativeai as genai

genai.configure(api_key="AIzaSyCXRRkJ6Uez-Lm5c0cxqP9YNRhwsE_hYGE")

model = genai.get_tuned_model(f'tunedModels/generate-num-7807')
model2 = genai.GenerativeModel(model_name=f'tunedModels/generate-num-7807')
result = model2.generate_content('how can i book tickets')

webhook_url_post = "https://sameerarora.app.n8n.cloud/webhook-test/989cb120-9ab9-425b-8a48-99c351bba433"



def response_generator(prompt):
    result = model2.generate_content(prompt)
    response = random.choice(
        [
            result.text
        ]
    )
    for word in response.split():
        yield word + " "
        time.sleep(0.05)


st.title("Ai chatbot")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("What is up?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    data_for_post = {"role": "user", "content": prompt}
    r = requests.post(webhook_url_post,json.dumps(data_for_post),headers = {'Content-Type':'application/json'})

    # Display message 
    with st.chat_message("user"):
        st.markdown(prompt)

    # Display response 
    with st.chat_message("assistant"):
        
        response = st.write_stream(response_generator(prompt))
   
    st.session_state.messages.append({"role": "assistant", "content": response})

