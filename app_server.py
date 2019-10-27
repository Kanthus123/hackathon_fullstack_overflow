import os
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
from flask import send_from_directory
from rekognition_connection import Rekognition as rk

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg'}

app = Flask(__name__)
app.secret_key = b'secret key'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024
rk = rk()


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/")
def login():
    return render_template('login.html')


@app.route("/", methods=['POST'])
def auth():
    usuarios = ['paulo.csm@outlook.com', 'batata123']
    username = request.form['username']
    password = request.form['password']

    if username not in usuarios or password not in usuarios:
        print("entrou")
        flash("Email ou Senha incorreto")
        return redirect('/')
    else:
        return redirect('/index', code=302)


@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    return render_template('cadastro.html')


@app.route('/index', methods=['GET', 'POST'])
def index():
    return render_template('report.html')


@app.route('/missing_person', methods=['POST'])
def missing_person_upload():
    flag = "pessoa_perdida"
    nome_idoso = "Jose"
    nome_parente = "Felipe Printes"

    if request.method == 'POST':
        # Checa se a requisição post tem um pedaço do arquivo
        if 'file' not in request.files or 'file2' not in request.files:
            flash('No file part')
            return redirect('/')

        # Verefica se há algum arquivo para ser enviado
        file = request.files['file']
        file2 = request.files['file2']
        if file.filename == '' or file2.filename == '':
            flash('Nenhum arquivo selecionado para upload')
            return redirect('/')

        if file and allowed_file(file.filename) and file2 and allowed_file(file2.filename):
            mensagem = rk.upload(file, nome_idoso, flag, foto_parente=file2, nome_parente=nome_parente)
            flash(mensagem)
            return redirect('/')


@app.route('/cad_person', methods=['GET'])
def cad_person_upload():
    nome_idoso = request.form['cName2']
    email = request.form['cMail']
    nome_parente = request.form['cName']
    cpf = request.form['cDoc']
    flag = "cad_pessoa"

    if request.method == 'POST':
        # Checa se a requisição post tem um pedaço do arquivo
        if 'file' not in request.files:
            flash('No file part')
            return redirect('/')

        # Verefica se há algum arquivo para ser enviado
        file = request.files['file']
        if file.filename == '':
            flash('Nenhum arquivo selecionado para upload')
            return redirect('/')

        if file and allowed_file(file.filename):
            mensagem = rk.upload(file, nome_idoso, flag)
            flash(mensagem)
            return redirect('/')

    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''


if __name__=="__main__":
    app.secret_key = 'super secret key'
    app.run(debug=True)