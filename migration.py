# import MongoClient
from database import Database

db = Database()
collection = db.booksCollection()

books = [
    {
        "id": 1,
        "name":"Calculus With Fun",
        "category": "Maths",
        "rentPerDay": 20
    },
    {
        "id": 2,
        "name":"Julius Caesar",
        "category": "Play",
        "rentPerDay": 10
    },
    {
        "id": 3,
        "name":"Panch Tantra",
        "category": "Stories",
        "rentPerDay": 15
    },
    {
        "id": 4,
        "name":"Jungle Book",
        "category": "Stories",
        "rentPerDay": 10
    },
    {
        "id": 5,
        "name":"Ramayana",
        "category": "Poetry",
        "rentPerDay": 20
    },
    {
        "id": 6,
        "name":"Godaan",
        "category": "Novel",
        "rentPerDay": 10
    },
    {
        "id": 7,
        "name":"Prithviraj Raso",
        "category": "Poetry",
        "rentPerDay": 45
    },
    {
        "id": 8,
        "name":"History of War",
        "category": "History",
        "rentPerDay": 20
    },
    {
        "id": 9,
        "name":"Himalaya",
        "category": "Geography",
        "rentPerDay": 25
    },
    {
        "id": 10,
        "name":"Modern Science",
        "category": "Science",
        "rentPerDay": 10
    },
    {
        "id": 11,
        "name":"Atlas",
        "category": "Geography",
        "rentPerDay": 20
    },
    {
        "id": 12,
        "name":"Lucant English Grammar",
        "category": "English Grammar",
        "rentPerDay": 10
    },
    {
        "id": 13,
        "name":"Diary of a Wimpy Kid",
        "category": "Novel",
        "rentPerDay": 10
    },
    {
        "id": 14,
        "name":"Law Of Motion",
        "category": "Science",
        "rentPerDay": 20
    },
    {
        "id": 15,
        "name":"Human Body",
        "category": "Science",
        "rentPerDay": 10
    },
    {
        "id": 16,
        "name":"Mahabarat",
        "category": "Poetry",
        "rentPerDay": 55
    },
    {
        "id": 17,
        "name":"Akbar And Birbal",
        "category": "Comics",
        "rentPerDay": 20
    },
    {
        "id": 18,
        "name":"Jatak Kathaye",
        "category": "Story",
        "rentPerDay": 40
    },
    {
        "id": 19,
        "name":"Indian Recepies",
        "category": "Food",
        "rentPerDay": 10
    },
    {
        "id": 20,
        "name":"Science and Ghost",
        "category": "Science",
        "rentPerDay": 10
    }
]

for book in books:
    rec_id = collection.insert_one(book)
    print("Data inserted with record id ", book['id'])

