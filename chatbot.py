from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser  # default output from llm
import os
from dotenv import load_dotenv
import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
load_dotenv(dotenv_path="D:\forashi\OneDrive\Documents\SecureSheP\secureshep\Chatbot\.env")

os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")  # type: ignore
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")  # type:ignore

# Prompt template
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "you are a helpful assistant, response to use queries"),
        ("user", "Question:{question}"),
    ]
)

#streamlit inputs
st.title("langchain gemini chatbot")
input_text = st.text_input("What you want to ask?")
#gemini
llm=ChatGoogleGenerativeAI(model="gemini-1.5-flash") #type:ignore
output_parser=StrOutputParser()
chain=prompt|llm|output_parser
if input_text:
    st.write(chain.invoke({'question':input_text}))
