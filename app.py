from flask import Flask, request, jsonify
import os
from werkzeug.utils import secure_filename
from flask import render_template
from flask_cors import CORS  
import base64
from fpdf import FPDF

app = Flask(__name__)
CORS(app)

pdf = FPDF()
def create_pdf(fileData):
    pdf.add_page()
    pdf.set_font("Arial", size = 15)
 
    pdf.cell(200, 10, txt = str(fileData), 
         ln = 1, align = 'C')

    pdf.output("output.pdf")   
    print("PDF")


def read_file(image_path):
    with open(image_path, 'rb') as f:
        return (f.read())
    
def extract_text(data):
    import requests

    API_URL = "https://api-inference.huggingface.co/models/microsoft/trocr-large-stage1"
    headers = {"Authorization": "Bearer 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"}       
    response = requests.post(API_URL, headers=headers, data=data)
    return response.json()
def extract_text_data(filename):
    text = read_file(filename)
    if text is None:
        return jsonify({'error': 'file not found'})
    return extract_text(text)
@app.route('/upload', methods=['POST'])
def upload():
    print('uploading...')
    request_data = request.json
    image_data = request_data.get('file')
    image_bytes = base64.b64decode(image_data.split(',')[1])
    filename = 'uploaded.jpg'
    with open(filename, 'wb') as f:
        f.write(image_bytes)
    data =  extract_text_data(filename)
    print(data[0]['generated_text'])
    create_pdf(data[0]['generated_text'])    
    return jsonify({
            "text":extract_text_data(filename)
        })
    
    
if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0")

