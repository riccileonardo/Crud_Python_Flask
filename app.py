from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name)

# Configurações do banco de dados MySQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://127.0.0.1:root@localhost:3306/trabalho_conclusao'
db = SQLAlchemy(app)

class Usuario(db.Model):
    id_usuario = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(45), nullable=True)
    senha = db.Column(db.String(45), nullable=True)

class Transmissao(db.Model):
    id_transmissao = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(45), nullable=True)

class Classificacao(db.Model):
    id_classificacao = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(45), nullable=True)

class Tipo(db.Model):
    id_tipo = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(45), nullable=True)

class Marca(db.Model):
    id_marca = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(45), nullable=True)

class Veiculo(db.Model):
    idVeiculo = db.Column(db.Integer, primary_key=True, autoincrement=True)
    placa = db.Column(db.String(45), nullable=True)
    quilometragem = db.Column(db.String(45), nullable=True)
    cor = db.Column(db.String(45), nullable=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id_usuario'))
    id_transmissao = db.Column(db.Integer, db.ForeignKey('transmissao.id_transmissao'))
    id_classificacao = db.Column(db.Integer, db.ForeignKey('classificacao.id_classificacao'))
    id_tipo = db.Column(db.Integer, db.ForeignKey('tipo.id_tipo'))
    id_marca = db.Column(db.Integer, db.ForeignKey('marca.id_marca'))

@app.route('/processar', methods=['POST'])

def processar_formulario():
    if request.method == 'POST':
        # Obter os dados do formulário
        ano = request.form['ano']  
        placa = request.form['placa']
        modelo = request.form['modelo']
        quilometragem = request.form['quilometragem']
        cor = request.form['cor']
        marca = request.form['marca']
        transmissao = request.form['transmissao']
        classificacao = request.form['classificacao']
        tipo = request.form['tipo']

        # Crie uma instância do modelo Veiculo para inserir no banco de dados
        novo_veiculo = Veiculo(placa=placa, quilometragem=quilometragem, cor=cor, id_usuario=1, id_transmissao=1, id_classificacao=1, id_tipo=1, id_marca=1)

        try:
            # Adicionar o novo veículo ao banco de dados
            db.session.add(novo_veiculo)
            db.session.commit()
            return "Dados inseridos com sucesso no banco de dados!"
        except Exception as e:
            return "Erro ao inserir dados no banco de dados: " + str(e)
    else:
        return "Método de requisição inválido."

if __name__ == '__main__':
    app.run()
