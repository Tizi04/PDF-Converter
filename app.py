from flask import Flask, request, render_template, jsonify, send_file
from werkzeug.utils import secure_filename
import os
from convert_to_PDF import convertir_a_PDF
from io import BytesIO

app = Flask(__name__)


ALLOWED_EXTENSIONS = set(['docx', 'txt', 'jpg', 'png', 'jpeg'])

def allowed_file(file):
    file = file.split(".")
    if file[1] in ALLOWED_EXTENSIONS:
        return True
    return False

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=["POST"])
def upload():

    file = request.files["archivo"]

    filename = secure_filename(file.filename)

    if file and allowed_file(filename):

        file_in_memory = BytesIO(file.read())
        file_in_memory.seek(0)

        pdf_output = convertir_a_PDF(file_in_memory, filename)

        if pdf_output:
            return send_file(pdf_output, as_attachment=True, download_name=f"{filename.rsplit('.', 1)[0]}.pdf", mimetype="application/pdf}")
        else:
            return jsonify({'error': 'Error converting the file'}), 500
    
    return jsonify({'error': 'File type not allowed'})  

if __name__ == "__main__":
    app.run(debug=True,host="0.0.0.0")