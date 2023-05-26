from flask import Flask
from flask_restful import Resource, Api, reqparse
import pymongo

# Definições da API
app = Flask(__name__)
api = Api(app)

# Estabelecer uma conexão com o MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017")
# Selecionar o banco de dados
db = client["teste"]
# Selecionar a coleção
collection = db["teste_hotel"]


# Classe modelo de hotel, cria o objeto e transforma em JSON
class HotelModel:
    def __init__(self, hotel_id, nome, estrelas, diaria, cidade):
        self.hotel_id = hotel_id
        self.nome = nome
        self.estrelas = estrelas
        self.diaria = diaria
        self.cidade = cidade

    def json(self):
        return {
            'hotel_id': self.hotel_id,
            'nome': self.nome,
            'estrelas': self.estrelas,
            'diaria': self.diaria,
            'cidade': self.cidade
        }


class Hoteis(Resource):
    # Get de todos os hoteis da lista
    def get(self):
        # O valor 0 indica que o campo deve ser excluído do resultado
        resultados = collection.find({}, {'_id': 0})

        # Converter os documentos em uma lista
        hoteis = list(resultados)

        return hoteis


class Hotel(Resource):
    # Define os argumentos do hotel
    argumentos = reqparse.RequestParser()
    argumentos.add_argument('nome')
    argumentos.add_argument('estrelas')
    argumentos.add_argument('diaria')
    argumentos.add_argument('cidade')

    # Classe criada para encontrar o hotel com base no ID
    def find_hotel(hotel_id):
        hotel = collection.find_one({'hotel_id': hotel_id})
        if hotel:
            del hotel['_id']
            return hotel
        return None

    # Get (buscar) do hotel com base no ID
    def get(self, hotel_id):
        # Usa a classe find hotel para encontrar o hotel com o ID informado
        hotel = Hotel.find_hotel(hotel_id)
        # Se o hotel existir, ele retorna, se não exibe a mensagem de erro
        if hotel:
            return hotel
        return {'message': 'Hotel não encontrado.'}, 404

    # Post (enviar) do hotel informado
    def post(self, hotel_id):
        dados = Hotel.argumentos.parse_args()

        # Forma simplificada de criar o novo hotel e passar os dados como arg
        hotel_objeto = HotelModel(hotel_id, **dados)  # kwargs
        novo_hotel = hotel_objeto.json()

        # Cria o novo hotel e passa os dados como argumento
        # novo_hotel = {
        #    'hotel_id': hotel_id,
        #    'nome': dados['nome'],
        #    'estrelas': dados['estrelas'],
        #    'diaria': dados['diaria'],
        #    'cidade': dados['cidade']
        # }

        # Inserir vários documentos de uma vez
        collection.insert_one(novo_hotel)
        del novo_hotel['_id']

        return novo_hotel, 200

    # Put (atualizar) do hotel com base no ID informado
    def put(self, hotel_id):
        dados = Hotel.argumentos.parse_args()

        # Atribui a variavel os argumento
        novo_hotel = {'hotel_id': hotel_id, **dados}
        # **dados é uma representação do kwargs, que desmembra os argumentos.
        # Facilitando a utilização dos argumentos e mantendo o código limpo.

        hotel = Hotel.find_hotel(hotel_id)

        # Se o hotel existir ele atualiza, se não ele cria um novo hotel
        if hotel:
            # Constrói a query de atualização usando o operador $set
            query = {'hotel_id': hotel['hotel_id']}
            update = {'$set': novo_hotel}

            # Executa a atualização usando o método update_one()
            # Sendo query a condição para atualizar e update o que atualizara.
            collection.update_one(query, update)

            hotel.update(novo_hotel)
            return hotel, 200

        # hoteis.append(novo_hotel)
        collection.insert_one(novo_hotel)
        del novo_hotel['_id']

        return novo_hotel, 201

    # Delete (exclui) o hotel informado
    def delete(self, hotel_id):
        resultado = collection.delete_one({'hotel_id': hotel_id})

        if resultado.deleted_count > 0:
            return {'message': 'Hotel deletado.'}, 200
        else:
            return {'message': 'Hotel não encontrado.'}, 404


# Cria os caminhos da API para serem chamadas
api.add_resource(Hoteis, '/hoteis')
api.add_resource(Hotel, '/hoteis/<string:hotel_id>')

if __name__ == '__main__':
    app.run(debug=True)
