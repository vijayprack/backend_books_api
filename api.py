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
    start_from = args.get('start_from')
    end_to = args.get('end_to')
    where = {}

    if book_name and person_name:
        where = {"book_name": {"$regex" : book_name, "$options" : 'i'} } 
        where = {"person_name": {"$regex" : person_name, "$options" : 'i'} }
    elif book_name :
        where = {"book_name": {"$regex" : book_name, "$options" : 'i'} }
    elif person_name:
        where = {"person_name": {"$regex" : person_name, "$options" : 'i'} }

    if start_from and end_to:
        where["issued_date"] = { "$gte": start_from, "$lte": end_to }
    elif start_from:
        where["issued_date"] = { "$gte": int(start_from) }
    elif end_to:
        where["issued_date"] = { "$lte": int(end_to) }

    try:
        data = transactions_collection.find(where)
        result = json.loads(json_util.dumps(data))
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
    filter = { 'book_name': book_name , 'person_name': person_name }
    
    try:  
        outputs = getTransactions()
        for output in outputs:
            if output['book_name'] == book_name and output['person_name'] == person_name:
                bookName = output['book_name']
                personName = output['person_name']
                issuedDate = output['issued_date']
                returnDate = output['return_date']
                break

        issuedDate = issuedDate[0:10]
        lst1 = issuedDate.split('/' or '/0')
        year1 = int(lst1[0])
        month1 = int(lst1[1])
        day1 = int(lst1[2])
        date1 = date(year1,month1,day1)

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
        data['total_rent'] = rent
        total_rent = data['total_rent']

        currentDateTime = datetime.now()
        data['return_date'] = currentDateTime.strftime("%Y/%m/%d %H:%M:%S")
        return_date = data['return_date']

        newvalue = { "$set": { 'return_date': return_date, 'total_rent': total_rent } }
        transactions_collection.update_one(filter, newvalue)

        return jsonify({"book name" : bookName,
                        "person name": personName,
                        "issued date": issuedDate,
                        "return date": returnDate,
                        "days": days,
                        "rent per day": rentPerDay,
                        "total rent": rent})
    except:
        return jsonify('404 Not Found')


@app.route('/persons', methods = ['GET'])
def getPersonList():
    args = request.args
    book_name = args.get('book_name')

    try:
        where = {}
        if book_name:
            where = {"book_name": {"$regex" : book_name, "$options" : 'i'} }
        data = transactions_collection.find(where)
        results = json.loads(json_util.dumps(data))
        book = results[0]['book_name']

        count = 0
        persons = []
        currently_person_who_issued_book_count = 0
        currently_person_who_issued_book = []
        
        for result in results:
            person = result['person_name']
            persons.append(person)
            count += 1
            if 'return_date' not in result:
                person = result['person_name']
                currently_person_who_issued_book.append(person)
                currently_person_who_issued_book_count += 1
                

        return jsonify({
            "Book Name": book,
            "All Persons ": persons,
            "Total Person Count": count,
            "Currently Person Who Issued Book": currently_person_who_issued_book,
            "Currently Total Person Who Issued Book": currently_person_who_issued_book_count
            })
    except:
        return jsonify("404 Not Found")



@app.route('/rent', methods = ['GET'])
def getRent():
    args = request.args
    book_name = args.get('book_name')

    try:
        where = {}
        if book_name:
            where = {"book_name": {"$regex" : book_name, "$options" : 'i'} }
        data = transactions_collection.find(where)
        results = json.loads(json_util.dumps(data))
        book = results[0]['book_name']

        total_rent = 0
        for result in results:
            rent = result['total_rent']
            total_rent += rent
        return  jsonify({"Book Name": book, "Total Rent Generated By Book": total_rent})
    except:
        return jsonify("404 Not Found")


@app.route('/issuedBooks', methods = ['GET'])
def getBooksByPersonName():
    args = request.args
    book_name = args.get('person_name')

    try:
        where = {}
        if book_name:
            where = {"person_name": {"$regex" : book_name, "$options" : 'i'} }
        data = transactions_collection.find(where)
        results = json.loads(json_util.dumps(data))
        person = results[0]['person_name']

        books = []
        for result in results:
            book = result['book_name']
            books.append(book)
        return  jsonify({"Person Name": person, "All Issued Books": books})
    except:
         return jsonify("404 Not Found")


if __name__ == '__main__': 
    app.run(debug=True)
