from src.utils.exception import CustomException
from src.utils.logger import  logging

from groq import Groq
import os 
import sys
from dotenv import load_dotenv
load_dotenv()
from datetime import datetime

groq_api=os.getenv("GROK_API_KEY")

client=Groq(api_key=groq_api)

class TextGenerator:
    def __init__(self):
        pass

    def intiatetextgenerator(self,audio_path):
        try:
            timestamp = datetime.now().strftime("%Y-%m-%d_%I-%M-%S_%p")
            output_path=fr"C:\mini_project\data\{timestamp}.txt"


            with open(audio_path,"rb")as file:
                response=client.audio.transcriptions.create(
                                file=file,
                model="whisper-large-v3",   # Fastest STT on Groq
                response_format="text"
            )
            transcript_text = response
            logging.info("covert the video to audieo ")
            
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(transcript_text) 
            return output_path
        except Exception as e:
            CustomException(e,sys)

if __name__=="__main__":
    obj=TextGenerator()
    a=obj.intiatetextgenerator(audio_path=r"C:\mini_project\data\output_audio.wav")