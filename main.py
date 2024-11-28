import os
import openai
import pandas as pd
import PyPDF2
from flask import Flask, request, jsonify, send_file
from werkzeug.utils import secure_filename
import psycopg2
import xlwt
from datetime import datetime
import logging

# إعدادات OpenAI
openai.api_key = 'your-openai-api-key'

# إعداد Flask
app = Flask(__name__)

# إعداد قاعدة البيانات (PostgreSQL)
DB_HOST = 'localhost'
DB_NAME = 'engineering_data'
DB_USER = 'your-db-user'
DB_PASSWORD = 'your-db-password'

def connect_db():
    conn = psycopg2.connect(
        host=DB_HOST, 
        database=DB_NAME, 
        user=DB_USER, 
        password=DB_PASSWORD
    )
    return conn

# مسار تحميل ملفات PDF
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# تحديد امتدادات الملفات المسموح بها
ALLOWED_EXTENSIONS = {'pdf'}

# وظيفة للتحقق من امتداد الملف
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# وظيفة لتحميل واستخراج النصوص من ملف PDF
def extract_text_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ''
        for page in reader.pages:
            text += page.extract_text()
    return text

# وظيفة لفتح ملف PDF واستخراج المعلومات باستخدام النماذج الذكية
def process_pdf_with_models(pdf_text):
    # استخدام LLaMA والنماذج الأخرى لتحليل النص
    response = openai.Completion.create(
        model="gpt-4", 
        prompt=f"Extract key information from this technical PDF:\n\n{pdf_text}",
        max_tokens=1500
    )
    return response.choices[0].text.strip()

# وظيفة لحفظ الدردشات في قاعدة البيانات
def save_chat_to_db(user_input, model_output):
    conn = connect_db()
    cursor = conn.cursor()
    query = "INSERT INTO chats (user_input, model_output, timestamp) VALUES (%s, %s, %s)"
    cursor.execute(query, (user_input, model_output, datetime.now()))
    conn.commit()
    cursor.close()
    conn.close()

# وظيفة لحفظ البيانات إلى ملف Excel
def save_to_excel(data, filename):
    workbook = xlwt.Workbook()
    sheet = workbook.add_sheet('Results')
    sheet.write(0, 0, 'User Input')
    sheet.write(0, 1, 'Model Output')
    
    for idx, (user_input, model_output) in enumerate(data, start=1):
        sheet.write(idx, 0, user_input)
        sheet.write(idx, 1, model_output)
    
    excel_file_path = f"{UPLOAD_FOLDER}/{filename}.xls"
    workbook.save(excel_file_path)
    return excel_file_path

# مسار رفع ملفات PDF
@app.route('/upload', methods=['POST'])
def upload_pdf():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # استخراج النصوص من ملف PDF
        pdf_text = extract_text_from_pdf(filepath)
        
        # معالجة النص باستخدام النماذج
        model_output = process_pdf_with_models(pdf_text)
        
        # حفظ الدردشة في قاعدة البيانات
        save_chat_to_db(pdf_text, model_output)
        
        return jsonify({
            "message": "File processed successfully",
            "model_output": model_output
        }), 200
    else:
        return jsonify({"error": "Invalid file format"}), 400

# مسار استرجاع الدردشات السابقة
@app.route('/chats', methods=['GET'])
def get_chats():
    conn = connect_db()
    cursor = conn.cursor()
    query = "SELECT user_input, model_output FROM chats ORDER BY timestamp DESC"
    cursor.execute(query)
    chats = cursor.fetchall()
    conn.close()
    
    # تحويل الدردشات إلى صيغة JSON
    chat_data = [{"user_input": chat[0], "model_output": chat[1]} for chat in chats]
    return jsonify(chat_data)

# مسار تحميل نتائج الدردشة على هيئة ملف Excel
@app.route('/export', methods=['GET'])
def export_to_excel():
    conn = connect_db()
    cursor = conn.cursor()
    query = "SELECT user_input, model_output FROM chats ORDER BY timestamp DESC"
    cursor.execute(query)
    chats = cursor.fetchall()
    conn.close()

    # تحويل الدردشات إلى ملف Excel
    chat_data = [{"user_input": chat[0], "model_output": chat[1]} for chat in chats]
    excel_file_path = save_to_excel(chat_data, 'chat_results')
    
    return send_file(excel_file_path, as_attachment=True)

# مسار إغلاق التطبيق مع سؤال الحفظ
@app.route('/close', methods=['POST'])
def close_app():
    user_input = request.json.get('user_input')
    if user_input:
        save_chat_to_db(user_input, 'Session Ended')  # حفظ الدردشة الأخيرة
    return jsonify({"message": "Goodbye! Your data has been saved."}), 200

if __name__ == '__main__':
    # إعداد سجل الأخطاء
    logging.basicConfig(level=logging.DEBUG)
    app.run(debug=True)
