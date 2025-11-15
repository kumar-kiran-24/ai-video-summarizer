from src.utils.exception import CustomException
from src.utils.logger import logging

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter
import sys

class PdfConverter:
    def __init__(self):
        pass

    def pdfconverter(self, file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                input_text = f.read()
            input_text = input_text.replace("**", "")

            output_pdf_path = r"C:\mini_project\data\final_notes.pdf"
            styles = getSampleStyleSheet()
            doc = SimpleDocTemplate(output_pdf_path, pagesize=letter)

            story = []
            for line in input_text.split("\n"):
                story.append(Paragraph(line, styles["Normal"]))
                story.append(Spacer(1, 12))
            doc.build(story)

            logging.info(f"PDF generated at: {output_pdf_path}")
            print(f"PDF saved at: {output_pdf_path}")
            return output_pdf_path

        except Exception as e:
            raise CustomException(e, sys)


if __name__ == "__main__":
    converter = PdfConverter()
    converter.pdfconverter(
        file_path=r"C:\mini_project\data\generated_notes.txt"
    )
