import os
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId 

app = Flask(__name__)
app.config["MONGO_DBNAME"] = 'cook-book-db'
app.config["MONGO_URI"] = 'mongodb+srv://root:r00tUser@cluster2-6phdr.mongodb.net/cook-book-db?retryWrites=true&w=majority'

mongo = PyMongo(app)


@app.route('/')
# @app.route('/get_recipes')
# def get_recipe():
#     return render_template("recipes.html", recipes=mongo.db.recipes.find())

# Add recipe
@app.route('/add_recipe')
def add_recipe():
    return render_template('add-recipe.html',
        difficulty=mongo.db.difficulty.find(), categories=mongo.db.categories.find(), cuisines=mongo.db.cuisines.find())  

# Filters
@app.route('/list_recipes', methods=["GET", "POST"])
def list_recipes():
    categories = mongo.db.categories.find()
    ingredients = mongo.db.ingredients.find()
    cuisines = mongo.db.cuisines.find()
    recipe = mongo.db.recipes.find()
    
    filters = {}
    if request.method == "POST":
        categories = request.form.get("categories")
        if not categories == None:
            filters["category_type"] = categories
        ingredient = request.form.getlist("ingredients")
        origin = request.form.get("cuisines")
        if not cuisines == None:
            filters["cuisines"] = cuisines
        
        filter_recipes = mongo.db.recipes.find({"$and": [filters, {"ingredients": {"$nin": ingredient}}]})
        filter_recipes_count = filter_recipes.count() 
        print(filter_recipes_count)
        return render_template('home.html', categories=categories, cuisines=cuisines, ingredients=ingredients, recipes=filter_recipes, count=filter_recipes_count)
    else:
        recipes = mongo.db.recipes.aggregate([
                {"$sort": {"category_type": -1}}
        ])
      
        return render_template('home.html', recipes=recipes, categories=categories, cuisines=cuisines, ingredients=ingredients)


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)
            
