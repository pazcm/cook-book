from flask import Flask, flash, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from dotenv import load_dotenv
import os
# import logging
from bson.objectid import ObjectId

# Load environment variables from .env
load_dotenv()

app = Flask(__name__)

# MongoDB Atlas connection
# app.config['MONGO_DBNAME'] = 'Cluster0-cookBook'
# MONGO_URI store in environment for security
app.config["MONGO_URI"] = os.getenv("MONGO_URI")
mongo = PyMongo(app)

@app.route('/')
def home():
    try:
        return render_template('home.html')
    except Exception as e:
        app.logger.error(f'Error occurred: {str(e)}')
        return 'An error occurred', 500

@app.route('/get_recipes')
def get_recipes():
    return render_template('recipes.html', recipes=mongo.db.recipes.find())


# Add recipe
@app.route('/add_recipe')
def add_recipe():
    return render_template('add-recipe.html',
        difficulty=mongo.db.difficulty.find(), categories=mongo.db.categories.find(), cuisines=mongo.db.cuisines.find())

# Insert recipe
@app.route('/insert_recipe', methods=["POST"])
def insert_recipe():
    image_url = request.form.get('image')
    print(f"Image URL: {image_url}")  # Check if the correct URL is submitted
    print(request.form) 
    recipes = mongo.db.recipes
    recipes.insert_one(  {
        'image_url': request.form.get('image'),
        'name': request.form.get('name'),
        'description': request.form.get('description'),
        'author': request.form.get('author'),
        'category': request.form.get('category_type'),
        'cuisine': request.form.get('cuisine'),
        'serves':request.form.get('serves'),
        'readyIn':request.form.get('readyIn'),
        'difficulty':request.form.get('mode'),
        'ingredients':request.form.get('ingredient'),
        'instructions':request.form.get('instructions'),
        'tips': request.form.get('tips')
        })
    return redirect(url_for('get_recipes'))
    
# Edit recipe
@app.route('/edit_recipe/<recipes_id>')
def edit_recipe(recipes_id):
    the_recipe =  mongo.db.recipes.find_one({'_id': ObjectId(recipes_id)})
    category_type =  mongo.db.categories.find()
    cuisine = mongo.db.cuisines.find()
    difficulty = mongo.db.difficulty.find()
    return render_template('edit-recipe.html', recipes=the_recipe,
                    categories=category_type, cuisines=cuisine, difficulty=difficulty)
                           
# Update recipe
@app.route('/update_recipe/<recipes_id>', methods=["GET", "POST"])
def update_recipe(recipes_id):
    recipes = mongo.db.recipes

    updated_fields = {
        'image_url': request.form.get('image'),
        'name': request.form.get('name'),
        'description': request.form.get('description'),
        'author': request.form.get('author'),
        'category': request.form.get('category_type'),
        'cuisine': request.form.get('cuisine'),
        'serves': request.form.get('serves'),
        'readyIn': request.form.get('readyIn'),
        'difficulty': request.form.get('mode'),
        'ingredients': request.form.get('ingredient'),
        'instructions': request.form.get('instructions'),
        'tips': request.form.get('tips')
    }

    # use $set to update only the provided fields | prevents the entire document from being replaced
    recipes.update_one(
        {'_id': ObjectId(recipes_id)},
        {'$set': updated_fields}
    )

    return redirect(url_for('get_recipes'))

# Delete recipe
@app.route('/delete_recipe/<recipes_id>')
def delete_recipe(recipes_id):
    mongo.db.recipes.delete_one({'_id': ObjectId(recipes_id)})
    return redirect(url_for('get_recipes'))
    
# Recipe detail
@app.route('/recipe_detail/<recipes_id>')
def recipe_detail(recipes_id):
    return render_template('recipe-detail.html', recipe=mongo.db.recipes.find_one({'_id':ObjectId(recipes_id)}))

# All recipes with filters
@app.route('/all_recipes', methods=["GET", "POST"])
def all_recipes():

    category = mongo.db.categories.find()
    cuisine = mongo.db.cuisines.find()
    difficulty = mongo.db.difficulty.find()
    filters = {}
    filtered_results = mongo.db.recipes.find(filters)
    
    if request.method == "POST":
        recipe_category = request.form.get('category_type')
        if not recipe_category == None:
            filters['category'] = recipe_category
            
        recipe_cuisine = request.form.get('cuisine')
        if not recipe_cuisine == None:
            filters['cuisine'] = recipe_cuisine
        
        recipe_difficulty = request.form.get('difficulty')
        if not recipe_difficulty == None:
            filters['difficulty'] = recipe_difficulty
          
        return render_template('results.html', recipes=filtered_results, categories=category, cuisines=cuisine, difficulty=difficulty)

    return render_template('all-recipes.html', recipes = mongo.db.recipes.find(), categories=category, cuisines=cuisine, difficulty=difficulty)

# Search box
@app.route('/search_box/', methods=["POST"])
def search_box():
    search = request.form['q']
    if (search != ''):
        return redirect(url_for('results', q=search))
    else:
        return render_template('recipes.html', recipes = mongo.db.recipes.find())

# Search results
@app.route('/results/<q>')
def results(q):
    results = mongo.db.recipes.find(
        {'$text': {'$search': q}})
    return render_template('results.html', recipes=results)
    
# Filters
@app.route('/list_recipes', methods=["GET", "POST"])
def list_recipes():
    category = mongo.db.categories.find()
    cuisine = mongo.db.cuisines.find()
    difficulty = mongo.db.difficulty.find()
    filters = {}
    filtered_results = mongo.db.recipes.find(filters)
    
    if request.method == "POST":
        recipe_category = request.form.get('category_type')
        if not recipe_category == None:
            filters['category'] = recipe_category
            
        recipe_cuisine = request.form.get('cuisine')
        if not recipe_cuisine == None:
            filters['cuisine'] = recipe_cuisine
        
        recipe_difficulty = request.form.get('difficulty')
        if not recipe_difficulty == None:
            filters['difficulty'] = recipe_difficulty
          
        return render_template('results.html', recipes=filtered_results, categories=category, cuisines=cuisine, difficulty=difficulty)
    else:
       return render_template('home.html', categories=category, cuisines=cuisine, difficulty=difficulty)
    
# check the connection to MongoDB
@app.route('/test_db_connection')
def test_db_connection():
    try:
        # Attempt to retrieve the first document from the 'recipes' collection
        recipe = mongo.db.recipes.find_one()
        if recipe:
            return f"Connected to MongoDB! Found a recipe: {recipe['name']}", 200
        else:
            return "Connected to MongoDB, but no recipes found.", 200
    except Exception as e:
        return f"Failed to connect to MongoDB: {str(e)}", 500

print("Mongo URI:", os.getenv("MONGO_URI"))

# if __name__ == '__main__':
#     app.run(host=os.environ.get('IP'),
#             port=int(os.environ.get('PORT')),
#             debug=True)

if __name__ == '__main__':
    app.run(debug=True)
