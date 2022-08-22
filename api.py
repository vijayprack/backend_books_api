from flask import Flask, request
from flask_restful import Resource, Api
from database import Database
from bson import json_util
import json

app = Flask(__name__)
api = Api(app)

db = Database()
collection = db.booksCollection()

class Book(Resource):
    def get(self, id):
        book = collection.find_one({"id": id})
        return json.loads(json_util.dumps(book))

class BookList(Resource):
    def get(self):
        args = request.args
        name = args.get('name')
        min_price = args.get('min_price')
        max_price = args.get('max_price')
        category = args.get('category')
        where = {}
        if name:
            where = {"name": {"$regex" : name, "$options" :'i'} }
        
        if min_price and max_price:
            where["rentPerDay"] = { "$gte": int(min_price), "$lte": int(max_price) }
        elif min_price:
            where["rentPerDay"] = { "$gte": int(min_price) }
        elif max_price:
            where["rentPerDay"] = { "$lte": int(max_price) }
        
        if category:
            where["category"] = {"$regex" : category, "$options" :'i'}
        
        print(where)
        book = collection.find(where)
        return json.loads(json_util.dumps(book))


api.add_resource(Book, '/books/<int:id>')
api.add_resource(BookList, '/books')

if __name__ == '__main__':
    app.run(debug=True)
