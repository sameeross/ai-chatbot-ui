import streamlit as st
import random
import time
import requests
import json

from http.server import BaseHTTPRequestHandler, HTTPServer

class WebhookHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        # Get the client’s IP address
        client_ip = self.client_address[0]
        print(f"Request received from IP: {client_ip}")

        # Read the data
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)

        # Assuming the webhook sends JSON data
        try:
            webhook_data = json.loads(post_data.decode('utf-8'))
            print("Received Webhook Data:", webhook_data)
        except json.JSONDecodeError:
            print("Error: Could not decode JSON data.")
        
        # Send a response back
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(b'{"status": "success"}')

# Start the HTTP server
def run(server_class=HTTPServer, handler_class=WebhookHandler, port=8080):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting server on port {port}...')
    httpd.serve_forever()

if __name__ == "__main__":
    run()

webhook_url_post = "https://sameerarora.app.n8n.cloud/webhook-test/989cb120-9ab9-425b-8a48-99c351bba433"


# Streamed response emulator
def response_generator():
    response = random.choice(
        [
            "Hello there! How can I assist you today?" + server_address,
            "Hi, human! Is there anything I can help you with?" + server_address,
            "Do you need help?" + server_address,
        ]
    )
    for word in response.split():
        yield word + " "
        time.sleep(0.05)


st.title("Ai chatbot")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("What is up?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    data_for_post = {"role": "user", "content": prompt}
    r = requests.post(webhook_url_post,json.dumps(data_for_post),headers = {'Content-Type':'application/json'})

    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        response = st.write_stream(response_generator())
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})


