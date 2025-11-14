from src.utils.exception import CustomException
from src.utils.logger import logging

from langchain_groq import ChatGroq
from langchain.schema import HumanMessage
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate
import os
import sys
from dotenv import load_dotenv
load_dotenv()

groq_api=os.getenv("GROK_API_KEY")
llm = ChatGroq(
    groq_api_key=os.getenv("GROQ_API_KEY"),
    model="mixtral-8x7b-32768"
)

class NotesGenerator:
    def __init__(self):
        pass

    def notesgenerator(self,file_path):
        try:
            ANALYSIS_PROMPT = """
You are an advanced analysis AI.

Given the following INPUT TEXT:

--------------------
{text}
--------------------

Generate the following:

1. **Summary** – A clean summary in 5–8 lines  
2. **Main Topics Covered** – Bullet points  
3. **Goal of the Text** – What the author wants to achieve  
4. **Line-by-line Interpretation** – Explain each sentence in simple words  
5. **Question & Answer Pairs** – Minimum 5 Q&A  
6. **Conclusion** – Final takeaway  
7. **What You Learn From This** – Key learnings list  

Make the output well-structured, clear, and formatted.
"""
            
        except Exception as e:
            CustomException(e,sys)
