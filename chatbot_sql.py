from langgraph.graph import StateGraph , START , END
from typing import TypedDict , Annotated
from langchain_openai import ChatOpenAI
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage , HumanMessage , SystemMessage
from dotenv import load_dotenv
#from langgraph.checkpoint.memory import SqliteSaver
from langgraph.checkpoint.sqlite import SqliteSaver
import sqlite3

load_dotenv()
llm = ChatOpenAI(model = 'gpt-4o-mini')

class ChatState(TypedDict):
    messages : Annotated[list[BaseMessage], add_messages]

graph =  StateGraph(ChatState)

def chat_node(state: ChatState):
    messages = state['messages']
    response = llm.invoke(messages)
    return {'messages' : [response]}


conn = sqlite3.connect(database='chat.db', check_same_thread=False)
checkpointer = SqliteSaver(conn = conn)    
    
graph.add_node('chat_node', chat_node)
graph.add_edge(START , 'chat_node')
graph.add_edge('chat_node' , END)

chatbot = graph.compile(checkpointer=checkpointer)

CONFIG = {'configurable': {'thread_id' : 'thread-1'}}
response = chatbot.invoke(
    {'messages' : [HumanMessage(content= 'Hey my name is dhruv')]},
    config = CONFIG
)
print(response)
