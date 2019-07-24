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
def get_recipes():
    return render_template("recipes.html", recipes=mongo.db.recipes.find())

# Add recipe
@app.route('/add_recipe')
def add_recipe():
    return render_template('add-recipe.html',
        difficulty=mongo.db.difficulty.find(), categories=mongo.db.categories.find(), cuisines=mongo.db.cuisines.find())

# Insert recipe
@app.route('/insert_recipe', methods=['POST'])
def insert_recipe():
    recipes = mongo.db.recipes
    recipes.insert_one(  {
        'image': request.form.get('image'),
        'name': request.form.get('name'),
        'description': request.form.get('description'),
        'author': request.form.get('author'),
        'category': request.form.get('type'),
        'cuisine': request.form.get('origin'),
        'serves':request.form.get('serves'),
        'readyIn':request.form.get('readyIn'),
        'difficulty':request.form.getlist('mode'),
        'ingredients':request.form.getlist('ingredient'),
        'instructions':request.form.get('instructions'),
        'tips': request.form.get('tips')
        })
    return redirect(url_for('get_recipes'))

# Edit recipe
@app.route('/edit_recipe/<recipes_id>')
def edit_recipe(recipes_id):
    the_recipe =  mongo.db.recipes.find_one({'_id': ObjectId(recipes_id)})
    all_categories =  mongo.db.categories.find()
    return render_template('edit-recipe.html', recipes=the_recipe,
                           categories=all_categories)
                           
# Update recipe
@app.route('/update_recipe/<recipes_id>', methods=['POST'])
def update_recipe(recipes_id):
    
    recipes = mongo.db.recipes
    recipes.update( {'_id': ObjectId(recipes_id)},
        {
        'image': request.form.get('image'),
        'name': request.form.get('name'),
        'description': request.form.get('description'),
        'author': request.form.get('author'),
        'category': request.form.get('type'),
        'cuisine': request.form.get('origin'),
        'serves':request.form.get('serves'),
        'readyIn':request.form.get('readyIn'),
        'difficulty':request.form.getlist('mode'),
        'ingredients':request.form.getlist('ingredient'),
        'instructions':request.form.get('instructions'),
        'tips': request.form.get('tips')
        })
    return redirect(url_for('get_recipes'))

# Delete recipe
@app.route('/delete_recipe/<recipes_id>')
def delete_recipe(recipes_id):
    mongo.db.recipes.remove({'_id': ObjectId(recipes_id)})
    return redirect(url_for('get_recipes'))
    
    
# ecipe detail
# @app.route('/recipe_detail')
# def recipe_detail():
#     return render_template('recipe-detail.html')
    

# Filters
@app.route('/list_recipes', methods=['GET', 'POST'])
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
            
