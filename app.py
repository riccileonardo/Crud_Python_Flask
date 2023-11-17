from flask import Flask, request, render_template, redirect, url_for, session
import mysql.connector # Biblioteca para conexão  e consulta do banco MySQL
import hashlib # Biblioteca para criptografar senha

app = Flask(__name__)
app.secret_key = '123123'

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
@app.route('/home')
def index():
    # Verifica se o usuário está logado
    if 'username' in session: #se o username estiver na sessão, ele vai para a pagina inicial
        return render_template('home.html')
    else:
        return redirect('/login')
    
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST': #se o metodo for post, ele vai pegar o username e a senha e vai verificar se existe no banco
        email = request.form['email'] #pega o username do formulario (resquest.form é o formulario submetido dentro do html | username é o nome do campo do formulario)
        password = encrypt_password(request.form['password']) #pega a senha do formulario e criptografa ela
        cursor.execute("SELECT * FROM usuario WHERE email = %s AND senha = %s", (email, password)) #executa o comando sql para selecionar o usuario e a senha
        user = cursor.fetchone() #retorna o usuario e a senha
        if user:
            session['username'] = email #se o usuario existir, ele vai criar uma sessão com o username
            return redirect('/')
        else:
            return "Login inválido. <a href='/login'>Tente novamente</a>"
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/login')

@app.route('/veiculos') # -----------------------------------------> Corrigido para '/veiculos' em vez de '/veiculos_html'
def veiculos(): #--------------------------------------------------> Corrigido para 'veiculos' em vez de 'veiculos_html' 
    if 'username' in session: #------------------------------------> Se o username estiver na sessão, ele vai para a pagina inicial
        cursor.execute("SELECT * FROM veiculo") # -----------------> Executa o comando SQL para selecionar todos os carros (execute eu pego a terra)
        veiculos = cursor.fetchall() # ----------------------------> Retorna todos os carros cadastrados (fetchall eu descarrego a terra)
        return render_template('veiculos.html', veiculos=veiculos) # Corrigido para 'veiculos' em vez de 'veiculos_html'
    else:
        return redirect('/login')
    
@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if 'username' in session:
        if request.method == 'POST':
            ano = request.form['ano']
            placa = request.form['placa']
            modelo = request.form['modelo']
            quilometragem = request.form['quilometragem']
            cor = request.form['cor']
            marca = request.form['marca']
            transmissao = request.form['transmissao']
            classificacao = request.form['classificacao']
            tipo = request.form['tipo']
            cursor.execute("INSERT INTO veiculo (ano, placa, modelo, quilometragem, cor, marca, transmissao, classificacao, tipo) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)", (ano, placa, modelo, quilometragem, cor, marca, transmissao, classificacao, tipo))
            db.commit()
            return redirect('/veiculos')
        return render_template('/cadastro.html')
    else:
        return redirect('/login')


@app.route('/relatorios', methods=['GET', 'POST'])
def relatorio():
    if 'username' in session:
        if request.method == 'POST':
            data_inicio = request.form['data_inicio']
            data_fim = request.form['data_fim']
            cursor.execute("SELECT * FROM aluguel WHERE data_inicio BETWEEN %s AND %s", (data_inicio, data_fim))
            relatorios = cursor.fetchall()
            return render_template('relatorios.html', relatorios=relatorios)
        return render_template('relatorios.html')

if __name__ == '__main__':
    app.run(debug=True)


