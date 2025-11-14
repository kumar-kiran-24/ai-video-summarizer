from src.utils.exception import CustomException
from src.utils.logger import logging

from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import os
import sys
from dotenv import load_dotenv

load_dotenv()

# ----------------- PROMPT TEMPLATE -----------------
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", """
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
""")
    ]
)

# ----------------- LLM INITIALIZATION -----------------
llm = ChatGroq(
    groq_api_key=os.getenv("GROK_API_KEY"),
    model="llama-3.1-8b-instant"
)

parser = StrOutputParser()


class NotesGenerator:
    def __init__(self):
        pass

    def notesgenerator(self, file_path, output_path):
        try:
            # Read the text from input file
            with open(file_path, "r", encoding="utf-8") as f:
                input_text = f.read()

            # Fill prompt template
            final_prompt = prompt.format(text=input_text)

            # LLM Call
            response = llm.invoke([HumanMessage(content=final_prompt)])
            notes_text = response.content

            # Save to .txt file
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(notes_text)

            logging.info(f"Notes successfully generated and saved at: {output_path}")
            print(f"Notes saved at: {output_path}")

            return output_path

        except Exception as e:
            raise CustomException(e, sys)


# ----------------- RUN DIRECTLY -----------------
if __name__ == "__main__":
    generator = NotesGenerator()
    generator.notesgenerator(
        file_path=r"C:\mini_project\data\transcript.txt",
        output_path=r"C:\mini_project\data\generated_notes.txt"
    )
