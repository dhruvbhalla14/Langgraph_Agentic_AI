import streamlit as st
from langgraph_backend import chatbot
from langchain_core.messages import HumanMessage
import uuid

# ----------------- utitlity funactions ---------------------
def generate_thread_id():
    thread = uuid.uuid4()
    return thread 

CONFIG = {'configurable': {'thread_id': 'thread_1'}}
#st.session_state is a dictionary in the stream lit which do not get refresh when pressing enter


#------------------- Session Setup -----------------------------

if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []
    
if 'thread_id' not in st.session_state:
    st.session_state['thread_id'] = generate_thread_id()     
    

#--------------------- Side Bar UI -----------------------------
st.sidebar.title('LangGraph Chatbot')
st.sidebar.button('New Chat')
st.sidebar.header('My Conversation')

for message in st.session_state['message_history']:
    with st.chat_message(message['role']):
        st.text(message['content'])
    
    
#{'role' : 'user', 'content' : 'Hi'}
#{'role' : 'assistant', 'content': 'Hello'}

user_input = st.chat_input('Type here')    

if user_input :
    
    #adding mesage to history 
    st.session_state['message_history'].append({'role' : 'user', 'content':user_input})
    with st.chat_message('user'):
        st.text(user_input)
        
    
    response = chatbot.invoke({'messages':[HumanMessage(content=user_input)]}, config= CONFIG)   
    ai_response = response['messages'][-1].content 
    st.session_state['message_history'].append({'role' : 'assistant', 'content':ai_response})    
    with st.chat_message('assistant'):
        st.text(ai_response) 