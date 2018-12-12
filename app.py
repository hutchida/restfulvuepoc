from flask import Flask, jsonify, request
from flask_cors import CORS
import uuid
import json

# configuration
DEBUG = True

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app)

# sanity check route
@app.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify('pong!')

#load json from local file
with open('data.json') as data_file:
    data_loaded = json.load(data_file)
#loop through json entries and add unique id before working with the data
#for entry in data_loaded:
#    entry['id'] = uuid.uuid4().hex

BOOKS = data_loaded

@app.route('/books', methods=['GET', 'POST'])
def all_books():
    response_object = {'status': 'success'}
    #ADD
    if request.method == 'POST':
        post_data = request.get_json()
        print('uuid generated then entry appended')
        BOOKS.append({
            'id': uuid.uuid4().hex,
            'title': post_data.get('title'),
            'author': post_data.get('author'),
            'read': post_data.get('read'),
            'isVisible': 'true'
        })
        response_object['message'] = 'Book added!'
        save_books(BOOKS)
    #DISPLAY
    else:
        response_object['books'] = BOOKS
        
    return jsonify(response_object)

@app.route('/books/<book_id>', methods=['PUT', 'DELETE'])
def single_book(book_id):
    response_object = {'status': 'success'}
    #UPDATE
    if request.method == 'PUT':
        post_data = request.get_json()
        remove_book(book_id)    
        BOOKS.append({
            'id': post_data.get('id'),
            'title': post_data.get('title'),
            'author': post_data.get('author'),
            'read': post_data.get('read'),
            'isVisible': post_data.get('isVisible')
        })
        response_object['message'] = 'Book updated!'
        save_books(BOOKS)
    #DELETE
    if request.method == 'DELETE':
        remove_book(book_id)
        response_object['message'] = 'Book removed!'
        save_books(BOOKS)
    return jsonify(response_object)

def remove_book(book_id):
    for book in BOOKS:
        if book['id'] == book_id:
            BOOKS.remove(book)
            return True
    return False

def save_books(BOOKS):
    with open('data.json', 'w') as outfile:
        json.dump(BOOKS, outfile, sort_keys = True, indent = 4, ensure_ascii = False)


if __name__ == '__main__':
    app.run()
