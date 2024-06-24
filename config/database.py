from pymongo import MongoClient

client = MongoClient("mongodb+srv://admin:admin@cluster0.e1hu4of.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")

db=client.person_db

collection_name = db["person_collection"]