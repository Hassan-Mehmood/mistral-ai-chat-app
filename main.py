import streamlit as st
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage

import dotenv
dotenv.load_dotenv('.env')

import os
api_key = os.getenv('MISTRAL_API_KEY')

st.set_page_config(
	page_title="Chat with Mistral AI",
)

st.title("Chat with Mistral AI")

if 'chat_messages' not in st.session_state:
	st.session_state.chat_messages = [
		ChatMessage(role='assistant' ,content="Hi, I'm Mistral AI. How can I help you today?")
	]

def get_mistral_client():
	return MistralClient(api_key=api_key)

for message in st.session_state.chat_messages:
	if message.role == 'user':
		with st.chat_message('User'):
			st.markdown(message.content)
	else:
		with st.chat_message('AI'):
			st.markdown(message.content)

# User input field
user_input = st.chat_input("Ask a question... ")

# Add user input to chat history
if user_input is not None and user_input.strip() != "":
	print(f'User: {user_input}')
	st.session_state.chat_messages.append(ChatMessage(role='user', content=user_input))

	with st.chat_message('Human'):
		st.markdown(user_input)

	with st.chat_message('AI'):
		client = get_mistral_client()
		
		response = client.chat(model='open-mixtral-8x7b', messages=st.session_state.chat_messages)
		response_content = response.choices[0].message.content

		print(f'Mistral AI: {response_content}')
		st.session_state.chat_messages.append(ChatMessage(role='assistant', content=response_content))
		st.markdown(response_content)