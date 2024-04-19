from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson import ObjectId
from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env file.

app = Flask(__name__)

# Set up MongoDB connection
client = MongoClient(os.getenv("MONGO_URI"))
db = client[os.getenv("MONGO_DBNAME")]
collection = db['ex']  # Assuming you have a collection called 'items'

@app.route('/')
def index():
    """Route to list all items - serves as the 'read' operation."""
    items = collection.find()
    return render_template('index.html', items=items)

@app.route('/create', methods=['GET', 'POST'])
def create():
    """Route to show the form and create a new item - serves as the 'create' operation."""
    if request.method == 'POST':
        item_data = {
            'name': request.form['name'],
            'price': request.form['price'],
            'quantity': request.form['quantity']
        }
        collection.insert_one(item_data)
        return redirect(url_for('index'))
    return render_template('create.html')

@app.route('/inventory')
def inventory():
    """Route to list all items."""
    items = collection.find()
    return render_template('inventory.html', items=items)

@app.route('/edit/<item_id>', methods=['GET', 'POST'])
def edit(item_id):
    """Route to edit an item - serves as the 'update' operation."""
    item_to_edit = collection.find_one({'_id': ObjectId(item_id)})
    if request.method == 'POST':
        updated_data = {
            'name': request.form['name'],
            'price': request.form['price'],
            'quantity': request.form['quantity']
        }
        collection.update_one({'_id': ObjectId(item_id)}, {'$set': updated_data})
        return redirect(url_for('index'))
    return render_template('edit.html', item=item_to_edit)

@app.route('/delete/<item_id>')
def delete(item_id):
    """Route to delete an item."""
    collection.delete_one({'_id': ObjectId(item_id)})
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
