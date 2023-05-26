import pymongo

Estabelecer uma conexão com o MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017")
Selecionar o banco de dados
db = client["teste"]
Selecionar a coleção
collection = db["teste_1"]

Inserir um único documento
documento = {"nome": "João", "bairro": "Santa Efigenia"}
collection.insert_one(documento)

Inserir vários documentos de uma vez
documentos = [
    {"nome": "Maria", "bairro": "Santa Terezinha"},
    {"nome": "Pedro", "bairro": "Santa Tereza"},
    {"nome": "Ana", "bairro": "Santa Clara"}
]
collection.insert_many(documentos)

Atualizar um único documento
filtro = {"nome": "João"}
novos_valores = {"$set": {"idade": 31}}
collection.update_one(filtro, novos_valores)

Atualizar vários documentos
filtro = {"nome": {"$lt": "Lua"}}
novos_valores = {"$inc": {"bairro": "Pampulha"}}
collection.update_many(filtro, novos_valores)

Excluir um único documento
filtro = {"nome": "João"}
collection.delete_one(filtro)

Excluir vários documentos
filtro = {"nome": {"$gt": "Lua"}}
collection.delete_many(filtro)

Consultar com filtro
filtro = {"nome": {"$gt": "Lua"}}
resultados = collection.find(filtro)

Consultar todos os documentos
resultados = collection.find()

Iterar pelos resultados
for documento in resultados:
    print(documento)

Documentação: https://pymongo.readthedocs.io/en/stable/