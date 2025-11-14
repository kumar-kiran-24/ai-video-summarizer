from src.utils.exception import CustomException
from src.utils.logger import logging

from moviepy.video.io.VideoFileClip import VideoFileClip
import sys

class audioconverter:
    def __init__(self):
        pass

    def intiate_audioconverter(self, video_path):
        try:
           
            audio_path = r"C:\mini_project\data\output_audio.wav"

            with VideoFileClip(video_path) as video:
                video.audio.write_audiofile(audio_path)

            print("Conversion done:", audio_path)
            logging.info(f"Video {video_path} converted to audio at {audio_path}")
            return audio_path

        except Exception as e:
            print("ERROR:", e)
            raise CustomException(e, sys)

if __name__ == "__main__":
    obj = audioconverter()
    result = obj.intiate_audioconverter(
        video_path=r"C:\vivo\Instagram\VID_20250426_221600_861.mp4"
    )
    print("Audio file saved at:", result)
