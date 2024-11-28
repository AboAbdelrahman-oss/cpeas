from flask import Flask, request, jsonify
from modules.pdf_processing import PDFProcessor
from models.llama_model import LlamaModel
from models.openai_model import OpenAIModel
import pandas as pd

app = Flask(__name__)

llama_model = LlamaModel()
openai_model = OpenAIModel(api_key="your-api-key")

@app.route('/ask', methods=['POST'])
def ask():
    data = request.get_json()
    question = data.get("question")
    pdf_file = data.get("pdf_file")

    if pdf_file:
        # معالجة ملف PDF
        processor = PDFProcessor(pdf_file)
        text = processor.extract_text()

        # توليد الرد من النماذج
        response_llama = llama_model.generate_response(text + " " + question)
        response_openai = openai_model.generate_response(text + " " + question)

        return jsonify({"response_llama": response_llama, "response_openai": response_openai})

    return jsonify({"error": "No PDF file provided!"}), 400

@app.route('/save_results', methods=['POST'])
def save_results():
    data = request.get_json()
    responses = data.get("responses")
    if responses:
        # حفظ النتائج في ملف Excel
        df = pd.DataFrame(responses)
        df.to_excel("responses.xlsx")
        return jsonify({"message": "Results saved successfully!"})
    return jsonify({"error": "No responses to save!"}), 400

if __name__ == "__main__":
    app.run(debug=True)
