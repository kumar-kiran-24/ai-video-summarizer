from src.utils.exception import CustomException
from src.utils.logger import logging

import os
import sys
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate
from pypdf import PdfReader

load_dotenv()

llm = ChatGroq(
    groq_api_key=os.getenv("GROK_API_KEY"),
    model="llama-3.1-8b-instant",streaming=True
)


class ChatBot:
    try:
        logging.info("chatbot is ready for the give the response")
        def __init__(self, txt_path):

            self.txt_path=txt_path
            with open(txt_path,"r",encoding="utf-8") as f:
                content_text=f.read()

            self.context = content_text
            self.history = []

        def ask(self, user_question):
            prompt_template = ChatPromptTemplate.from_messages([
                ("system", f"""
    You are a strict context-based chatbot.

    RULES:
    - Answer ONLY from the given PDF context.
    - If answer is not in the context → reply: "I don't know based on the context."
    - Use chat history for better answers.
    - Do NOT hallucinate.
    - Stay factual to the PDF.

    ----- PDF CONTEXT -----
    {self.context}
    ----- END CONTEXT -----
    """),
                *self.history,
                ("user", "{question}")
            ])


            final_prompt=prompt_template.invoke({"question": user_question})

            response = llm.invoke(final_prompt.to_messages())
            bot_reply = response.content
            self.history.append(HumanMessage(content=user_question))
            self.history.append(AIMessage(content=bot_reply))
            logging.info("reponse is ready")

            return bot_reply

        def reset(self):
            """Forget chat history for new session"""
            self.history = []
    except Exception as e:
        CustomException(e,sys)


if __name__ == "__main__":
    bot = ChatBot(r"C:\mini_project\data\final_notes.pdf")

    print(bot.ask("Give me the summary."))
    print(bot.ask("Explain the main idea."))

    bot.reset() 

    print(bot.ask("What are the topics?"))
