#poner la configuracion de mongo
from flask_pymongo import pymongo

DB_USER = "****"
DB_PASSWORD = "****"
DB_HOST = "******"
DB_NAME = "usuarios"


client = pymongo.MongoClient(f'mongodb+srv://{DB_USER}:{DB_PASSWORD}@{DB_HOST}.mongodb.net/{DB_NAME}?retryWrites=true&w=majority')
db_users=client.usuarios
