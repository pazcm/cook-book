import os
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId 

app = Flask(__name__)
app.config["MONGO_DBNAME"] = 'cook-book-db'
app.config["MONGO_URI"] = 'mongodb+srv://root:r00tUser@cluster2-6phdr.mongodb.net/cook-book-db?retryWrites=true&w=majority'

mongo = PyMongo(app)


@app.route('/')
@app.route('/get_recipes')
def get_recipe():
    return render_template("recipes.html", recipes=mongo.db.recipes.find())
    
# Search box










if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)
            
