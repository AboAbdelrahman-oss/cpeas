from PyPDF2 import PdfReader

class PDFProcessor:
    def __init__(self, file_path):
        self.file_path = file_path
        self.text = ""

    def extract_text(self):
        # استخراج النص من ملف PDF
        with open(self.file_path, 'rb') as file:
            reader = PdfReader(file)
            text = ""
            for page in reader.pages:
                text += page.extract_text()
        self.text = text
        return self.text
