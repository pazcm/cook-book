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

    
# Filters
@app.route('/list_recipes', methods=["GET", "POST"])
def list_recipes():
    category = mongo.db.category.find()
    ingredient = mongo.db.ingredient.find()
    cuisine = mongo.db.cuisine.find()
    recipes = mongo.db.recipes.find()
    
    filters = {}
    if request.method == "POST":
        recipe_category = request.form.get("category")
        if not recipe_category == None:
            filters["category_type"] = recipe_category
        recipe_ingredient = request.form.getlist("ingredient")
        recipe_cuisine = request.form.get("cuisine")
        if not recipe_cuisine == None:
            filters["cuisine_origin"] = recipe_cuisine
        
        filter_recipes = mongo.db.recipes.find({"$and": [filters, {"ingredient": {"$nin": recipe_ingredient}}]})
        filter_recipes_count = filter_recipes.count() 
        print(filter_recipes_count)
        return render_template('home.html', category=category, cuisine=cuisine, ingredient=ingredient, recipes=filter_recipes, count=filter_recipes_count)
    else:
        recipes = mongo.db.recipes.aggregate([
                {"$sort": {"category_type": -1}}
        ])
      
        return render_template('home.html', recipes=recipes, category=category, cuisine=cuisine, ingredient=ingredient)










if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)
            
