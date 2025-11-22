from flask import Flask, request, jsonify, send_file, render_template
from flask_cors import CORS
import os
import uuid
from main import Main
from src.chabot.chatbot import ChatBot

app = Flask(__name__)
CORS(app)

# Folders
UPLOAD_FOLDER = "data/uploads"
RESULT_FOLDER = "data/results"
LAST_TEXT_PATH = None   
CD = None              

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)



@app.route("/")
def home():
    return render_template("index.html")




@app.route("/upload-video", methods=["POST"])
def upload_video():
    global LAST_TEXT_PATH

    if "video" not in request.files:
        return jsonify({"error": "No video file provided"}), 400

    file = request.files["video"]
    filename = f"{uuid.uuid4()}.mp4"
    video_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(video_path)

    try:
        main_ = Main()
        pdf_path, text_path = main_.main(video_path=video_path)

        LAST_TEXT_PATH = text_path

        safe_name = f"video_summary_{uuid.uuid4().hex}.pdf"
        return send_file(
    pdf_path,
    as_attachment=True,
    download_name=safe_name
)

    except Exception as e:
        return jsonify({"error": str(e)}), 500



@app.route("/youtube-to-pdf", methods=["POST"])
def youtube_to_pdf():
    global LAST_TEXT_PATH

    data = request.get_json(force=True)
    youtube_link = data.get("link")

    if not youtube_link:
        return jsonify({"error": "YouTube link required!"}), 400

    try:
        main_ = Main()
        pdf_path, text_path = main_.youtube_link(youtube_link)

        LAST_TEXT_PATH = text_path

        return send_file(
            pdf_path,
            as_attachment=True,
            download_name="youtube_summary.pdf"
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/chat", methods=["POST"])
def chat():
    global LAST_TEXT_PATH
    global CD

    if LAST_TEXT_PATH is None:
        return jsonify({"error": "Upload a video or process YouTube link first."}), 400

    if CD is None:
        CD = ChatBot(txt_path=LAST_TEXT_PATH)

    data = request.get_json(force=True)
    message = data.get("message", "")

    try:
        response = CD.ask(message)
        return jsonify({"response": response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/reset-chat", methods=["POST"])
def reset_chat():
    global CD
    CD = None
    return jsonify({"status": "chatbot reset"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
