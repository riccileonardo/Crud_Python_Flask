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

# Função para pegar o id do usuário para depois eu usar.
def get_user_id(username):
    cursor.execute("SELECT id_usuario FROM usuario WHERE email = %s", (username,))
    result = cursor.fetchone()
    if result:
        return result[0]
    else:
        return None

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
            session['username'] = email # ------------------------> Se o usuario existir, ele vai criar uma sessão com o username
            return redirect('/') # --------------------------------> Redireciona para a pagina inicial
        else:
            return "Login inválido. <a href='/login'>Tente novamente</a>"
    return render_template('login.html')

@app.route('/logout') # ------------------------------------------> Corrigido para '/logout' em vez de '/logout_html'
def logout(): #---------------------------------------------------> Corrigido para 'logout' em vez de 'logout_html'
    session.pop('username', None) # ------------------------------> Se o username estiver na sessão, ele vai para a pagina inicial
    return redirect('/login') # ----------------------------------> Redireciona para a pagina de login

@app.route('/veiculos') # -----------------------------------------> Corrigido para '/veiculos' em vez de '/veiculos_html'
def veiculos(): #--------------------------------------------------> Corrigido para 'veiculos' em vez de 'veiculos_html' 
    if 'username' in session: #------------------------------------> Se o username estiver na sessão, ele vai para a pagina inicial
        cursor.execute("""
            SELECT
                veiculo.id_veiculo AS id_veiculo,
                usuario.nome AS nome_usuario,
                marca.nome AS marca_veiculo,
                veiculo.ano AS ano_veiculo,
                veiculo.placa AS placa_veiculo,
                veiculo.modelo AS modelo_veiculo,
                veiculo.quilometragem AS quilometragem_veiculo,
                veiculo.cor AS cor_veiculo,
                transmissao.nome AS transmissao_veiculo,
                classificacao.nome AS classificacao_veiculo,
                tipo.nome AS tipo_do_veiculo
            FROM
                veiculo
                JOIN usuario ON veiculo.id_usuario = usuario.id_usuario
                JOIN marca ON veiculo.id_marca = marca.id_marca
                JOIN transmissao ON veiculo.id_transmissao = transmissao.id_transmissao
                JOIN classificacao ON veiculo.id_classificacao = classificacao.id_classificacao
                JOIN tipo ON veiculo.id_tipo = tipo.id_tipo
        """)
 #----> Executa o comando SQL para selecionar todos os carros (execute eu pego a terra)
        veiculos = cursor.fetchall() # ----------------------------> Retorna todos os carros cadastrados (fetchall eu descarrego a terra)
        return render_template('veiculos.html', veiculos=veiculos) # Corrigido para 'veiculos' em vez de 'veiculos_html'
    else: # -------------------------------------------------------> Se o username não estiver na sessão, ele vai para a pagina de login
        return redirect('/login') # -------------------------------> Redireciona para a pagina de login
    
@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if 'username' in session:
        if request.method == 'POST':
            id_usuario = get_user_id(str(session['username']))
            ano = request.form['ano']
            placa = request.form['placa']
            modelo = request.form['modelo']
            quilometragem = request.form['quilometragem']
            cor = request.form['cor']
            id_marca = request.form['id_marca']
            id_transmissao = request.form['id_transmissao']
            id_classificacao = request.form['id_classificacao']
            id_tipo = request.form['id_tipo']
            cursor.execute("""
            INSERT INTO veiculo (ano, placa, modelo, quilometragem, cor, id_marca, id_transmissao, id_classificacao, id_tipo, id_usuario)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (ano, placa, modelo, quilometragem, cor, id_marca, id_transmissao, id_classificacao, id_tipo, id_usuario))
            db.commit()
            return redirect('/veiculos')
        
        cursor.execute("SELECT id_transmissao, nome from transmissao")
        transmissao = cursor.fetchall()
        cursor.execute("SELECT id_classificacao, nome from classificacao")
        classificacao = cursor.fetchall()
        cursor.execute("SELECT id_tipo, nome from tipo")
        tipo = cursor.fetchall()
        cursor.execute("SELECT id_marca, nome from marca")
        marca = cursor.fetchall()
        return render_template('/cadastro.html', transmissoes=transmissao, classificacoes=classificacao, tipos=tipo, marcas=marca)
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
    
@app.route('/veiculos/<id_veiculo>/delete', methods=['POST'])
def excluir(id_veiculo):
    if 'username' in session:
        cursor.execute("DELETE FROM veiculo WHERE id_veiculo = %s", (id_veiculo,))
        db.commit()
        return redirect('/veiculos')

@app.route('/veiculos/<id_veiculo>/editar', methods=['GET', 'POST'])
def editar(id_veiculo):
    if 'username' in session:
        if request.method == 'POST':
            ano = request.form['ano']
            placa = request.form['placa']
            modelo = request.form['modelo']
            quilometragem = request.form['quilometragem']
            cor = request.form['cor']
            id_marca = request.form['id_marca']
            id_transmissao = request.form['id_transmissao']
            id_classificacao = request.form['id_classificacao']
            id_tipo = request.form['id_tipo']
            cursor.execute("""
                UPDATE veiculo
                SET ano = %s, placa = %s, modelo = %s, quilometragem = %s, cor = %s,
                id_marca = %s, id_transmissao = %s, id_classificacao = %s, id_tipo = %s
                WHERE id_veiculo = %s
                """, (ano, placa, modelo, quilometragem, cor, id_marca, id_transmissao, id_classificacao, id_tipo, id_veiculo)
            )
            db.commit()
            return redirect('/veiculos')
        
        cursor.execute("SELECT * FROM veiculo WHERE id_veiculo = %s", (id_veiculo,))
        veiculo = cursor.fetchone()
        cursor.execute("SELECT id_transmissao, nome from transmissao")
        transmissao = cursor.fetchall()
        cursor.execute("SELECT id_classificacao, nome from classificacao")
        classificacao = cursor.fetchall()
        cursor.execute("SELECT id_tipo, nome from tipo")
        tipo = cursor.fetchall()
        cursor.execute("SELECT id_marca, nome from marca")
        marca = cursor.fetchall()
        return render_template('editar.html', transmissoes=transmissao, classificacoes=classificacao, tipos=tipo, marcas=marca, veiculo=veiculo)


if __name__ == '__main__':
    app.run(debug=True)


