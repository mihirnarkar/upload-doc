from flask import Flask, request, render_template
from werkzeug.utils import secure_filename
import os
from docx import Document
import fitz  # PyMuPDF library for PDF processing

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'doc', 'docx', 'pdf'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            return render_template('index.html', message='No file part')

        files = request.files.getlist('file')

        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        return render_template('index.html', message='Files uploaded successfully!')

    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    combined_text = ""

    for filename in os.listdir(app.config['UPLOAD_FOLDER']):
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)

        if filename.endswith(('.doc', '.docx')):
            doc = Document(filepath)
            for paragraph in doc.paragraphs:
                combined_text += paragraph.text + '\n'

        elif filename.endswith('.pdf'):
            with fitz.open(filepath) as pdf_document:
                for page_num in range(pdf_document.page_count):
                    page = pdf_document[page_num]
                    combined_text += page.get_text() + '\n'

    with open(os.path.join(app.config['UPLOAD_FOLDER'], 'combined_text.txt'), 'w', encoding='utf-8') as output_file:
        output_file.write(combined_text)

    return render_template('index.html', message='Text file created successfully!')

if __name__ == '__main__':
    app.run(debug=True)
