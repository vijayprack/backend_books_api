from pymongo import MongoClient
from os import getenv


class Database:
    __CONNECTION_STRING__ = getenv('MONGODB_URL')
    __db__ = None
    
    def __connect__(self):
        try:
            client = MongoClient(self.__CONNECTION_STRING__)
            print("Connecting to MongoDB database!!")
            self.__db__ = client['library']
            print("Connecting to database `library`!!")
        except:
            print("Could not connect to MongoDB!!")
        
    def booksCollection(self):
        self.__connect__()
        return self.__db__.books

    def transactionsCollection(self):
        self.__connect__()
        return self.__db__.transactions

