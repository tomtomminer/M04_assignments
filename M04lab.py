from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
db = SQLAlchemy(app)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_name = db.Column(db.String(100))
    author = db.Column(db.String(100))
    publisher = db.Column(db.String(100))

@app.route('/books')
def get_books():

    books = Book.query.all()

    output = []
    for book in books:
        book_data = {
            'id': book.id,
            'book_name': book.book_name,
            'author': book.author,
            'publisher': book.publisher
        }
        output.append(book_data)

    return {'books': output}

@app.route('/books/<id>')
def get_book(id):

    book = Book.query.get_or_404(id)
    return {
        'id': book.id,
        'book_name': book.book_name,
        'author': book.author,
        'publisher': book.publisher
    }

@app.route('/books', methods=['POST'])
def add_book():

    book = Book(
        book_name=request.json['book_name'],
        author=request.json['author'],
        publisher=request.json['publisher']
    )
    db.session.add(book)
    db.session.commit()
    return {
        'message': 'Book added'
    }

@app.route('/books/<id>', methods=['PUT'])
def update_book(id):

    book = Book.query.get_or_404(id)
    book.book_name = request.json['book_name']
    book.author = request.json['author']
    book.publisher = request.json['publisher']
    db.session.commit()
    return {
        'message': 'Book updated'
    }

@app.route('/books/<id>', methods=['DELETE'])
def delete_book(id):

    book = Book.query.get(id)

    if book is None:
        return {
            'error': 'Book not found'
        }
    
    db.session.delete(book)
    db.session.commit()
    return {
        'message': 'Book deleted'
    }