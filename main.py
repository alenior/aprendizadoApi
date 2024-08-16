from flask import Flask, make_response, jsonify, request
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

# Configuração da conexão com o MySQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:password@localhost/dbApiCarros'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.sort_keys = False

db = SQLAlchemy(app)

# Definindo o modelo Carro, que corresponde à tabela já existente no MySQL
class Carro(db.Model):
    __tablename__ = 'carros'  # Nome da tabela no MySQL
    id = db.Column(db.Integer, primary_key=True)
    marca = db.Column(db.String(50), nullable=False)
    modelo = db.Column(db.String(50), nullable=False)
    ano = db.Column(db.Integer, nullable=False)

# Rota para obter a lista de carros
@app.route('/carros', methods=['GET'])
def get_carros():
    # Consulta todos os carros no banco de dados
    carros = Carro.query.all()
    carros_list = [{
        'id': carro.id,
        'marca': carro.marca,
        'modelo': carro.modelo,
        'ano': carro.ano
    } for carro in carros]

    return make_response(
        jsonify(
            mensagem='Lista de carros',
            dados=carros_list
        )
    )

# Rota para obter um carro específico pelo ID
@app.route('/carros/<int:id>', methods=['GET'])
def get_carro(id):
    carro = Carro.query.get(id)
    if carro:
        return make_response(
            jsonify(
                mensagem='Detalhes do carro',
                carro={
                    'id': carro.id,
                    'marca': carro.marca,
                    'modelo': carro.modelo,
                    'ano': carro.ano
                }
            )
        )
    else:
        return make_response(
            jsonify(
                mensagem='Carro não encontrado'
            ), 404
        )

# Rota para adicionar um novo carro
@app.route('/carros', methods=['POST'])
def create_carro():
    dados = request.json
    novo_carro = Carro(
        marca=dados['marca'],
        modelo=dados['modelo'],
        ano=dados['ano']
    )
    db.session.add(novo_carro)
    db.session.commit()

    return make_response(
        jsonify(
            mensagem='Carro cadastrado com sucesso!',
            carro={
                'id': novo_carro.id,
                'marca': novo_carro.marca,
                'modelo': novo_carro.modelo,
                'ano': novo_carro.ano
            }
        )
    )

# Rota para atualizar um carro específico pelo ID
@app.route('/carros/<int:id>', methods=['PUT'])
def update_carro(id):
    carro = Carro.query.get(id)
    if carro:
        dados = request.json
        carro.marca = dados.get('marca', carro.marca)
        carro.modelo = dados.get('modelo', carro.modelo)
        carro.ano = dados.get('ano', carro.ano)
        db.session.commit()

        return make_response(
            jsonify(
                mensagem='Carro atualizado com sucesso!',
                carro={
                    'id': carro.id,
                    'marca': carro.marca,
                    'modelo': carro.modelo,
                    'ano': carro.ano
                }
            )
        )
    else:
        return make_response(
            jsonify(
                mensagem='Carro não encontrado'
            ), 404
        )

# Rota para excluir um carro específico pelo ID
@app.route('/carros/<int:id>', methods=['DELETE'])
def delete_carro(id):
    carro = Carro.query.get(id)
    if carro:
        db.session.delete(carro)
        db.session.commit()

        return make_response(
            jsonify(
                mensagem='Carro excluído com sucesso!'
            )
        )
    else:
        return make_response(
            jsonify(
                mensagem='Carro não encontrado'
            ), 404
        )

if __name__ == '__main__':
    app.run()
