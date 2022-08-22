# import MongoClient
from pymongo import MongoClient
import os

class Database:
    __CONNECTION_STRING__ = os.getenv("MONGODB_URL")
    __db__ = None
    
    def __connect__(self):
        try:
            client = MongoClient(self.__CONNECTION_STRING__)
            print("Connecting to MongoDB database!")
        except:
            print("Could not connect to MongoDB!")

        self.__db__ = client['library']
        print("Connecting to database `library`!!")
        
    def booksCollection(self):
        self.__connect__()
        return self.__db__.books

    def transactionsCollection(self):
        self.__connect__()
        return self.__db__.books

