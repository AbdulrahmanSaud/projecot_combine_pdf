from flask import Flask, render_template, request, send_file, redirect, url_for
import os
from PyPDF2 import PdfMerger
from werkzeug.utils import secure_filename
import tempfile

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = tempfile.gettempdir()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        files = request.files.getlist('pdfs')
        pdf_paths = []
        for file in files:
            if file and file.filename.lower().endswith('.pdf'):
                filename = secure_filename(file.filename)
                path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(path)
                pdf_paths.append(path)
        if not pdf_paths:
            return 'No PDF files uploaded.', 400
        pdf_paths.sort()  # Sort alphabetically
        merger = PdfMerger()
        for pdf in pdf_paths:
            merger.append(pdf)
        output_path = os.path.join(app.config['UPLOAD_FOLDER'], 'combined_output.pdf')
        merger.write(output_path)
        merger.close()
        # Clean up uploaded files
        for pdf in pdf_paths:
            os.remove(pdf)
        return send_file(output_path, as_attachment=True, download_name='combined_output.pdf')
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True) 