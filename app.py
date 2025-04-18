from flask import Flask, flash, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from dotenv import load_dotenv
import os
# # import logging
from bson.objectid import ObjectId
# import dns.resolver


load_dotenv()

app = Flask(__name__)

MONGO_URI = os.getenv("MONGO_URI")
app.config["MONGO_URI"] = MONGO_URI
# app.config["MONGO_DBNAME"] = "cookBookDB"
print("Is Ok!! Loaded MONGO_URI:", MONGO_URI)

# mongo = PyMongo(app)
# print("Mongo DB Object:", mongo.db)  # DB not connected ??? (*)

mongo = PyMongo(app)
db = mongo.cx["cookBookDB"]  # access DB explicitly (*)
print("OK!!! Database object:", db)


@app.route('/')
def home():
    try:
        return render_template('home.html')
    except Exception as e:
        app.logger.error(f'Error occurred: {str(e)}')
        return 'An error occurred', 500

@app.route('/get_recipes')
def get_recipes():
    return render_template('recipes.html', recipes=db.recipes.find())

# Add recipe
@app.route('/add_recipe')
def add_recipe():
    return render_template('add-recipe.html',
        difficulty=db.difficulty.find(), categories=db.categories.find(), cuisines=db.cuisines.find())

# Insert recipe
@app.route('/insert_recipe', methods=["POST"])
def insert_recipe():
    image_url = request.form.get('image')
    print(f"Image URL: {image_url}")  # Check if the correct URL is submitted
    print(request.form) 
    recipes = db.recipes
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
    the_recipe =  db.recipes.find_one({'_id': ObjectId(recipes_id)})
    category_type =  db.categories.find()
    cuisine = db.cuisines.find()
    difficulty = db.difficulty.find()
    return render_template('edit-recipe.html', recipes=the_recipe,
                    categories=category_type, cuisines=cuisine, difficulty=difficulty)
                           
# Update recipe
@app.route('/update_recipe/<recipes_id>', methods=["GET", "POST"])
def update_recipe(recipes_id):
    recipes = db.recipes

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
    db.recipes.delete_one({'_id': ObjectId(recipes_id)})
    return redirect(url_for('get_recipes'))
    
# Recipe detail
@app.route('/recipe_detail/<recipes_id>')
def recipe_detail(recipes_id):
    return render_template('recipe-detail.html', recipe=db.recipes.find_one({'_id':ObjectId(recipes_id)}))

# All recipes with filters
@app.route('/all_recipes', methods=["GET", "POST"])
def all_recipes():

    category = db.categories.find()
    cuisine = db.cuisines.find()
    difficulty = db.difficulty.find()
    filters = {}
    filtered_results = db.recipes.find(filters)
    
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

    return render_template('all-recipes.html', recipes = db.recipes.find(), categories=category, cuisines=cuisine, difficulty=difficulty)

# Search box
@app.route('/search_box/', methods=["POST"])
def search_box():
    search = request.form['q']
    if (search != ''):
        return redirect(url_for('results', q=search))
    else:
        return render_template('recipes.html', recipes = db.recipes.find())

# Search results (MongoDB needs a text index on the fields you want to search)
@app.route('/results/<q>')
def results(q):
    results = db.recipes.find(
        {'$text': {'$search': q}})
    return render_template('results.html', recipes=results)

    
# Filters
@app.route('/list_recipes', methods=["GET", "POST"])
def list_recipes():
    category = db.categories.find()
    cuisine = db.cuisines.find()
    difficulty = db.difficulty.find()
    filters = {}
    
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
        
        # Query after building the filters
        filtered_results = db.recipes.find(filters)
          
        return render_template('results.html', recipes=filtered_results, categories=category, cuisines=cuisine, difficulty=difficulty)
    else:
       return render_template('home.html', categories=category, cuisines=cuisine, difficulty=difficulty)

   
# Testing --- check the connection to MongoDB
# http://127.0.0.1:5000/test_db_connection
@app.route('/test_db_connection')
def test_db_connection():
    try:
        # Attempt to retrieve the first document from the 'recipes' collection
        recipe = db.recipes.find_one()
        if recipe:
            return f"Connected to MongoDB! Found a recipe: {recipe['name']}", 200
        else:
            return "Connected to MongoDB, but no recipes found.", 200
    except Exception as e:
        return f"Failed to connect to MongoDB: {str(e)}", 500

# print("Mongo URI:", os.getenv("MONGO_URI"))
# print("!!! Loaded MONGO_URI:", os.getenv("MONGO_URI"))


# if __name__ == '__main__':
#     app.run(host=os.environ.get('IP'),
#             port=int(os.environ.get('PORT')),
#             debug=True)

if __name__ == '__main__':
    app.run(debug=True)

# def test_mongo_dns_lookup():
#     try:
#         answers = dns.resolver.resolve('_mongodb._tcp.cluster0-cookbook.6dnti.mongodb.net', 'SRV')
#         print("✅ DNS lookup succeeded. SRV records found:")
#         for answer in answers:
#             print(answer.to_text())
#     except Exception as e:
#         print("❌ DNS lookup failed:", e)

# # Call the function
# test_mongo_dns_lookup()