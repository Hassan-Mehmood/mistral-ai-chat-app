import streamlit as st
from langchain_core.messages import AIMessage, HumanMessage
from langchain_mistralai.chat_models import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

import dotenv
dotenv.load_dotenv('.env')

import os
api_key = os.getenv('MISTRAL_API_KEY')

st.set_page_config(
	page_title="Chat with Mistral AI",
)

st.title("Chat with Mistral AI")

# Checking if 'chat_history' exists in the session state
if 'chat_history' not in st.session_state:
	st.session_state.chat_history = [
		AIMessage(content="Hi, I'm Mistral AI. How can I help you today?")
	]

def get_sql_chain():
	chat = ChatMistralAI(model_name='open-mixtral-8x7b', api_key=api_key)
	
	prompt = ChatPromptTemplate.from_template("This is your chat history so far: {chat_history}. You are an asistant and you will answer questions. Here is the question: {question}")
	chain = prompt | chat | StrOutputParser()

	return chain

for message in st.session_state.chat_history:
	if isinstance(message, AIMessage):
		with st.chat_message('AI'):
			st.markdown(message.content)
	else:
		with st.chat_message('User'):
			st.markdown(message)

# User input field
user_input = st.chat_input("Ask a question... ")

# Add user input to chat history
if user_input is not None and user_input.strip() != "":
	st.session_state.chat_history.append(HumanMessage(content=user_input))

	with st.chat_message('Human'):
		st.markdown(user_input)

	with st.chat_message('AI'):
		sql_chain = get_sql_chain()
		response = sql_chain.invoke({
			'chat_history': st.session_state.chat_history,
			'question': user_input
		})
		st.session_state.chat_history.append(AIMessage(content=response))
		st.markdown(response)