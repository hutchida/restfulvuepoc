from flask import Flask, jsonify, request
from flask_cors import CORS
import uuid
import json

print('Server loading now...')
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
print('Data loaded...')

#loop through json entries and add unique id before working with the data
#for entry in data_loaded:
#    entry['id'] = uuid.uuid4().hex


# Filter python objects with list comprehensions
def FilterReadYes(data_loaded):
    return [x for x in data_loaded if x['read'] == True]
def FilterReadNo(data_loaded):
    return [x for x in data_loaded if x['read'] == False]
def FilterRangeOfEntries(data_loaded, lower, upper):
    return [x for x in data_loaded[lower:upper]]
#BOOKS = FilterReadYes(data_loaded)
#BOOKS = FilterReadNo(data_loaded)
#BOOKS = FilterRangeOfEntries(data_loaded,0,10)
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


#@app.route('/range?start=<lower>&pageSize=<pageSize>', methods=['GET'])
@app.route('/range', methods=['GET'])
def range_of_books():    
    lower = int(request.args.get('start'))
    upper = lower + int(request.args.get('size'))
    response_object = {'status': 'success'}
    response_object['books'] = FilterRangeOfEntries(data_loaded,lower,upper)
    return jsonify(response_object)

@app.route('/books/<book_id>', methods=['PUT', 'DELETE'])
def single_book(book_id):
    response_object = {'status': 'success'}
    #UPDATE
    print('Updating...' + book_id)
    if request.method == 'PUT':
        post_data = request.get_json()
        remove_book(book_id)    
        BOOKS.append({
            'lrid': post_data.get('lrid'),
            'pa': post_data.get('pa'),
            'searchterm': post_data.get('searchterm'),
            'title1': post_data.get('title1'),
            'location1': post_data.get('location1'),
            'type1': post_data.get('type1'),
            'title2': post_data.get('title2'),
            'location2': post_data.get('location2'),
            'type2': post_data.get('type2'),
            'title3': post_data.get('title3'),
            'location3': post_data.get('location3'),
            'type3': post_data.get('type3'),
            'isVisible': post_data.get('isVisible')
        })
        #print(BOOKS)
        response_object['message'] = 'Book updated!'
        save_books(BOOKS)
    #DELETE
    if request.method == 'DELETE':
        remove_book(book_id)
        response_object['message'] = 'Book removed!'
        save_books(BOOKS)
        
        #range_of_books() #call the display function to refresh the page after deletion
    return jsonify(response_object)

def remove_book(book_id):
    for book in BOOKS:
        print(book)
        if book['lrid'] == book_id:
            print(book)
            BOOKS.remove(book)
            print('Removed entry...', book['lrid'], book_id)
            return True
    return False

def save_books(BOOKS):
    with open('data.json', 'w') as outfile:
        json.dump(BOOKS, outfile, sort_keys = True, indent = 4, ensure_ascii = True)
        print('Saved...')


if __name__ == '__main__':
    app.run()
