from pymongo import MongoClient

class database:
    @staticmethod
    def getConnection(database=None):
        client = MongoClient('mongodb://muthumani:muthumani%40098@localhost:27017/?authSource=users',serverSelectionTimeoutMS=5000)
        if database is None:
            database=client['muthumani_Ecommerce']
            return database
        else:
            return client[database]