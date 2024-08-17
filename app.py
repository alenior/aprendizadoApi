from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:password@localhost/dbApiCarros'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.sort_keys = False

db = SQLAlchemy(app)

class Carro(db.Model):
    __tablename__ = 'carros'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    marca = db.Column(db.String(50), nullable=False)
    modelo = db.Column(db.String(50), nullable=False)
    ano = db.Column(db.Integer, nullable=False)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/consulta')
def consulta():
    return render_template('consulta.html')

@app.route('/cadastro')
def cadastro():
    return render_template('cadastro.html')  # Certifique-se que existe um cadastro.html

@app.route('/editar')
def editar():
    return render_template('editar.html')  # Certifique-se que existe um editar.html

@app.route('/excluir')
def excluir():
    return render_template('excluir.html')  # Certifique-se que existe um excluir.html

@app.route('/carros', methods=['GET'])
def get_carros():
    carros = Carro.query.all()
    carros_list = [{'id': carro.id, 'marca': carro.marca, 'modelo': carro.modelo, 'ano': carro.ano} for carro in carros]
    return jsonify(dados=carros_list)

# Rotas para outras funcionalidades: cadastro, edição e exclusão

if __name__ == '__main__':
    app.run()
