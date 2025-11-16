import os
from datetime import datetime
from yt_dlp import YoutubeDL

class AudioFromYT:
    def __init__(self):
        pass

    def audio(self, link):
        try:
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            output_folder = r"C:\mini_project\data\Youtube"
            os.makedirs(output_folder, exist_ok=True)
            temp_path = os.path.join(output_folder, f"{timestamp}.%(ext)s")

            ydl_opts = {
                "format": "bestaudio/best",
                "outtmpl": temp_path,

        
                "postprocessors": [],

                # clean logging
                "quiet": True,
                "no_warnings": True,
            }

            with YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(link, download=True)
            downloaded_file = ydl.prepare_filename(info)
            final_mp3 = downloaded_file.rsplit(".", 1)[0] + ".mp3"
            os.rename(downloaded_file, final_mp3)

            return final_mp3

        except Exception as e:
            print("Download error:", e)
            return None


if __name__ == "__main__":
    obj = AudioFromYT()
    res = obj.audio("https://www.youtube.com/watch?v=6M5VXKLf4D4")
    print(res)
