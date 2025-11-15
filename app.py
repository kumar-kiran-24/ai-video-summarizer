from flask import Flask, request, jsonify, send_file, render_template
from flask_cors import CORS
import os
import uuid
from main import Main
from src.chabot.chatbot import ChatBot

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "data/uploads"
RESULT_FOLDER = "data/results"
LAST_PDF_PATH = None

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)



@app.route("/")
def home_page():
    return render_template("index.html")



@app.route("/upload-video", methods=["POST"])
def upload_video():
    global LAST_TEXT_PATH
  

    if "video" not in request.files:
        return jsonify({"error": "No video file provided"}), 400

    file = request.files["video"]
    filename = str(uuid.uuid4()) + ".mp4"
    video_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(video_path)

    main_ = Main()
    pdf_path,text_path = main_.main(video_path=video_path)

    LAST_TEXT_PATH = text_path
    

    return send_file(pdf_path, as_attachment=True)



@app.route("/chat", methods=["POST"])
def chat():
    global  LAST_TEXT_PATH
    global CD

    if LAST_TEXT_PATH is None:
        return jsonify({"error": "Upload a video first!"}), 400

    CD=ChatBot(txt_path=LAST_TEXT_PATH)
    

    data = request.json
    message = data.get("message", "")
    response = CD.ask(message)

    return jsonify({"response": response})


@app.post("/reset-chat")
def reset_chat():
    global CD
 
    CD.reset()  # <-- reset conversation
    return {"status": "reset done"}


if __name__ == "__main__":
    app.run(debug=True)
