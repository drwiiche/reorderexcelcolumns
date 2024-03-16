from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
from werkzeug.utils import secure_filename

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = 'uploads/'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    
    file = request.files['file']
    
    if file.filename == '':
        return redirect(request.url)
    
    filename = secure_filename(file.filename)
    file.save(app.config['UPLOAD_FOLDER'] + filename)
    
    df = pd.read_excel(app.config['UPLOAD_FOLDER'] + filename)
    columns = df.columns.tolist()

    return render_template('upload.html', filename=filename, columns=columns)

@app.route('/reorder', methods=['POST'])
def reorder_columns():
    filename = request.form['filename']
    selected_columns = request.form.getlist('selected-columns')

    df = pd.read_excel(app.config['UPLOAD_FOLDER'] + filename)
    df = df[selected_columns]

    df.to_excel(app.config['UPLOAD_FOLDER'] + 'modified_' + filename, index=False)

    
    return "File saved successfully!"

if __name__ == '__main__':
    app.run(debug=True)
