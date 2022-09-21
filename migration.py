# import MongoClient
from database import Database

db = Database()
collection = db.booksCollection()

books = [
    {
        "name":"Calculus With Fun",
        "category": "Maths",
        "rentPerDay": 20
    },
    {
        "name":"Julius Caesar",
        "category": "Play",
        "rentPerDay": 10
    },
    {
        "name":"Panch Tantra",
        "category": "Stories",
        "rentPerDay": 15
    },
    {
        "name":"Jungle Book",
        "category": "Stories",
        "rentPerDay": 10
    },
    {
        "name":"Ramayana",
        "category": "Poetry",
        "rentPerDay": 20
    },
    {
        "name":"Godaan",
        "category": "Novel",
        "rentPerDay": 10
    },
    {
        "name":"Prithviraj Raso",
        "category": "Poetry",
        "rentPerDay": 45
    },
    {
        "name":"History of War",
        "category": "History",
        "rentPerDay": 20
    },
    {
        "name":"Himalaya",
        "category": "Geography",
        "rentPerDay": 25
    },
    {
        "name":"Modern Science",
        "category": "Science",
        "rentPerDay": 10
    },
    {
        "name":"Atlas",
        "category": "Geography",
        "rentPerDay": 20
    },
    {
        "name":"Lucant English Grammar",
        "category": "English Grammar",
        "rentPerDay": 10
    },
    {
        "name":"Diary of a Wimpy Kid",
        "category": "Novel",
        "rentPerDay": 10
    },
    {
        "name":"Law Of Motion",
        "category": "Science",
        "rentPerDay": 20
    },
    {
        "name":"Human Body",
        "category": "Science",
        "rentPerDay": 10
    },
    {
        "name":"Mahabarat",
        "category": "Poetry",
        "rentPerDay": 55
    },
    {
        "name":"Akbar And Birbal",
        "category": "Comics",
        "rentPerDay": 20
    },
    {
        "name":"Jatak Kathaye",
        "category": "Story",
        "rentPerDay": 40
    }, {
        "book_name":"",
        "person_name":"Vijay",
        "issued_date":"",
        "returned_date":"",
    },
    {
        "book_name":"",
        "person_name":"Raj",
        "issued_date":"",
        "returned_date":"",
    },
    {
        "book_name":"",
        "person_name":"Suresh",
        "issued_date":"",
        "returned_date":"",
    },
    {
        "book_name":"",
        "person_name":"Mukesh",
        "issued_date":"",
        "returned_date":"",
    },
    {
        "book_name":"",
        "person_name":"Ram",
        "issued_date":"",
        "returned_date":"",
    },
    {
        "book_name":"",
        "person_name":"Shyam",
        "issued_date":"",
        "returned_date":"",
    },
    {
        "book_name":"",
        "person_name":"Mohan",
        "issued_date":"",
        "returned_date":"",
    },
    {
        "book_name":"",
        "person_name":"Gudia",
        "issued_date":"15/5/2022",
        "returned_date":"",
    },
    {
        "name":"Indian Recepies",
        "category": "Food",
        "rentPerDay": 10
    },
    {
        "name":"Science and Ghost",
        "category": "Science",
        "rentPerDay": 10
    }
]

for book in books:
    rec_id = collection.insert_one(book)
    print("Data inserted with record name ", book['name'])


transactions_collection = db.transactionsCollection()

transactions = []

for transaction in transactions:
    rec_id = transactions_collection.insert_one(transaction)
    print("Data inserted with record person_name ", transaction['person_name'])

