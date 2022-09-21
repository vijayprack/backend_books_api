from distutils.log import error
from flask import Flask, request, jsonify
from flask_restful import Api
from database import Database
from bson import json_util, ObjectId
import json
from datetime import date, datetime

app = Flask(__name__)
api = Api(app)

db = Database()
collection = db.booksCollection()

@app.route('/books/<id>', methods = ['GET'])
def getBook(id):
    try:
        data = collection.find_one({'_id': ObjectId(str(id))})
        return json.loads(json_util.dumps(data))
    except:
        return jsonify("404 Not Found")

# @app.route('/book/<string:name>', methods = ['GET'])
# def getBookByName(name):
#     try:
#         data = collection.find_one({'name': name})
#         return json.loads(json_util.dumps(data))
#     except:
#         return jsonify("404 Not Found")

@app.route('/books', methods = ['GET'])
def getFilteredBooks():
    args = request.args
    name = args.get('name')
    min_price = args.get('min_price')
    max_price = args.get('max_price')
    category = args.get('category')
    where = {}
    if name:
        where = {"name": {"$regex" : name, "$options" : 'i'} }
    
    if min_price and max_price:
        where["rentPerDay"] = { "$gte": int(min_price), "$lte": int(max_price) }
    elif min_price:
        where["rentPerDay"] = { "$gte": int(min_price) }
    elif max_price:
        where["rentPerDay"] = { "$lte": int(max_price) }
    
    if category:
        where["category"] = {"$regex" : category, "$options" :'i'}
        
    try:
        book = collection.find(where)
        return json.loads(json_util.dumps(book))
    except:
        return jsonify("404 Not Found")


transactions_collection = db.transactionsCollection()

@app.route('/transactions/<id>', methods = ['GET'])
def getTransactionById(id):
    try:
        data = transactions_collection.find_one({'_id': ObjectId(str(id))})
        result = json.loads(json_util.dumps(data))
        return result
    except:
        return jsonify("404 Not Found")

@app.route('/transactions', methods = ['GET'])
def getTransactions():
    args = request.args
    book_name = args.get('book_name')
    person_name = args.get('person_name')
    where = {}
    if book_name:
        where = {"book_name": {"$regex" : book_name, "$options" : 'i'} }
    elif person_name:
        where['person_name'] = {"person_name": {"$regex" : person_name, "$options" : 'i'} }

    try:
        transactions = transactions_collection.find(where)
        result = json.loads(json_util.dumps(transactions))
        return result
    except:
        return jsonify("404 Not Found")


@app.route('/transactions', methods = ['POST'])
def issued():
    data = request.get_json()
    bookName = data['book_name']
    personName = data['person_name']
    currentDateTime = datetime.now()
    data['issued_date'] = currentDateTime.strftime("%Y/%m/%d %H:%M:%S")
    issuedDate = data['issued_date']

    try:
        if request.method == 'POST':
            transactions_collection.insert_one(data)
            response = jsonify(bookName, personName, issuedDate)
            response.status_code = 201
            return response
    except:
        return jsonify("404 Not Found")
        

@app.route('/transactions', methods = ["PATCH"])
def returnDate():
    data = request.get_json()
    book_name = data['book_name']
    person_name = data['person_name']
    currentDateTime = datetime.now()
    data['return_date'] = currentDateTime.strftime("%Y/%m/%d %H:%M:%S")
    return_date = data['return_date']

    filter = { 'book_name': book_name , 'person_name': person_name }
    newvalue = { "$set": { 'return_date': return_date } }
    
    try:
        if book_name and person_name:
            book_name = {"book_name": {"$regex" : book_name, "$options" : 'i'} }
            person_name = {"person_name": {"$regex": person_name, "$options": 'i'} }
            transactions_collection.update_one(filter, newvalue)
            
            output = getTransactions()
            bookName = output[0]['book_name']
            personName = output[0]['person_name']

            issuedDate = output[0]['issued_date']
            issuedDate = issuedDate[0:10]
            lst1 = issuedDate.split('/' or '/0')
            year1 = int(lst1[0])
            month1 = int(lst1[1])
            day1 = int(lst1[2])
            date1 = date(year1,month1,day1)

            returnDate = output[0]['return_date']
            returnDate = returnDate[0:10]
            lst2 = returnDate.split('/' or '/0')
            year2 = int(lst2[0])
            month2 = int(lst2[1])
            day2 = int(lst2[2])
            date2 = date(year2,month2,day2)

            days = str(date2 - date1)
            days = days.split(' ')
            days = int(days[0])
            days = days

            books = getFilteredBooks()
            for i in range(len(books)):
                if books[i]['name'] == bookName:
                    rentPerDay = books[i]['rentPerDay']

            rent = days * rentPerDay
   
            return jsonify({"book name" : bookName,
                            "person name": personName,
                            "issued date": issuedDate,
                            "return date": returnDate,
                            "days": days,
                            "rent per day": rentPerDay,
                            "total rent": rent})
    except error as e:
        return e


if __name__ == '__main__': 
    app.run(debug=True)
