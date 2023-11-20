from flask import Flask, render_template, request, redirect, session
import mysql.connector # Biblioteca para conexão  e consulta do banco MySQL
import hashlib # Biblioteca para criptografar senha

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta'

db = mysql.connector.connect( #db agora é a variavel do meu banco
    host="localhost",
    user="root",
    passwd="root",
    database="trabalho_conclusao"
)
cursor = db.cursor() #cursor é a variavel que vai executar os comandos(consulta, select, delete...) no banco

# Função para criptografar senha usando SHA-256
def encrypt_password(password):
    sha256 = hashlib.sha256()
    sha256.update(password.encode('utf-8'))
    return sha256.hexdigest() # Retorna a senha criptografada em hexadecimal

@app.route('/')
def index():
    # Verifica se o usuário está logado
    if 'username' in session: #se o username estiver na sessão, ele vai para a pagina inicial
        cursor.execute("SELECT * FROM carros") # Executa o comando SQL para selecionar todos os carros (execute eu pego a terra)
        carros = cursor.fetchall() # Retorna todos os carros cadastrados (fetchall eu descarrego a terra)
        return render_template('index.html', carros_html=carros) # Renderiza a página inicial com a lista de carros
    else:
        return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = encrypt_password(request.form['password'])
        cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
        user = cursor.fetchone()
        if user:
            session['username'] = username 
            return redirect('/')
        else:
            return "Login inválido. <a href='/login'>Tente novamente</a>"
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/login')

# Restante do código para adicionar e exibir carros permanece o mesmo
EOFErrorgv,afdgmadga,DeprecationWarning

adf,klgadçgmadçfgm,