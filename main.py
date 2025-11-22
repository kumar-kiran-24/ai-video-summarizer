from src.utils.logger import logging
from src.utils.exception import CustomException

from src.chabot.chatbot import ChatBot
from src.components.notes_generator import NotesGenerator
from src.datatransporter.audieocoverter import audioconverter
from src.datatransporter.pdfconverter import PdfConverter
from src.components.text_generater import TextGenerator
from src.datatransporter.youtudedata import AudioFromYT


class Main:
    def __init__(self):
        self.audeio = audioconverter()
        self.note_generator = NotesGenerator()
        self.pdf_converter = PdfConverter()
        self.text_generator = TextGenerator()
        self.pdf_converter=PdfConverter()
        self.youtube=AudioFromYT()
        
    
    def main(self, video_path):
        try:
            audeiopath = self.audeio.intiate_audioconverter(video_path=video_path)
            text_path = self.text_generator.intiatetextgenerator(audio_path=audeiopath)
            notes = self.note_generator.notesgenerator(file_path=text_path)
            pdf=self.pdf_converter.pdfconverter(file_path=notes)
    
            return pdf,text_path
        except Exception as e:
            raise CustomException(e)
        
    def youtube_link(self,link):
        try:
            youtube_to_audieo=self.youtube.audio(link=link)
            text_path = self.text_generator.intiatetextgenerator(audio_path=youtube_to_audieo)
            notes = self.note_generator.notesgenerator(file_path=text_path)
            pdf=self.pdf_converter.pdfconverter(file_path=notes)
            return pdf,text_path
        except Exception as e:
            raise CustomException(e)
    
        
      

            
            
if __name__ == "__main__":
    obj = Main()
    res = obj.main(video_path=r"C:\vivo\Instagram\VID_20250426_221600_861.mp4")
    print(res)
