from flask import Flask, flash, render_template, redirect, request, url_for, session
from flask_pymongo import PyMongo
from dotenv import load_dotenv
import os
from bson.objectid import ObjectId
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import User

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
# Configure secret key for session management
app.secret_key = os.getenv('SECRET_KEY')
if not app.secret_key:
    raise ValueError("No Flask SECRET_KEY set")

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'  # Redirect to 'login' view if not authenticated

@login_manager.user_loader
def load_user(user_id):
    user = db.users.find_one({"_id": ObjectId(user_id)})
    if not user:
        return None
    return User(user)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        users = db.users
        existing_user = users.find_one({'email': request.form['email']})

        if existing_user is None:
            hashpass = generate_password_hash(request.form['password'])
            users.insert_one({
                'author': request.form['author'],
                'email': request.form['email'],
                'password': hashpass
            })
            return redirect(url_for('login'))
        return 'Email already registered'
    return render_template('register.html')
    
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        form = request.form
        email = form.get('email')
        password = form.get('password')
        
        user_data = mongo.db.users.find_one({'email': email})
        if user_data:
            user = User(user_data) # in User class for flask-login

            if User.validate_login(user_data["password"], password):
                login_user(user) # flask-login login
                session["author"] = user.author # now stored in User class
                flash("Welcome back, " + user.author + "!", "success")
                return redirect(url_for('home'))
        
        flash('Invalid email or password', 'danger')
        return redirect(url_for('login'))
    
    # Handle GET request
    return render_template('login.html')

@app.route('/logout')
def logout():
    logout_user()
    session.clear() 
    flash("You have been logged out.", "info")
    return redirect(url_for('login'))

@app.route('/profile')
@login_required
def profile():
    # Pull info from MongoDB using current user
    user_data = mongo.db.users.find_one({"email": current_user.email})
    
    if not user_data:
        flash("User not found", "danger")
        return redirect(url_for("home"))
    
    return render_template("profile.html", user=user_data)

@app.route('/profile/edit', methods=['GET', 'POST'])
@login_required
def edit_profile():
    user_data = mongo.db.users.find_one({"email": current_user.email})
    
    if request.method == 'POST':
        new_author = request.form.get("author")
        new_bio = request.form.get("bio")

        mongo.db.users.update_one(
            {"email": current_user.email},
            {"$set": {"author": new_author, "bio": new_bio}}
        )

        session["author"] = new_author  # keep navbar updated
        flash("Profile updated successfully!", "success")
        return redirect(url_for("home"))

    return render_template("edit_profile.html", user=user_data)

# Configure MongoDB
MONGO_URI = os.getenv("MONGO_URI")
app.config["MONGO_URI"] = MONGO_URI

# Initialize MongoDB connection
mongo = PyMongo(app)
db = mongo.cx["cookBookDB"]  # access DB explicitly (*)

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
@login_required
def add_recipe():
    return render_template('add-recipe.html',
        difficulty=db.difficulty.find(), categories=db.categories.find(), cuisines=db.cuisines.find())

# Insert recipe
@app.route('/insert_recipe', methods=["POST"])
@login_required
def insert_recipe():
    recipes = db.recipes
    recipes.insert_one({
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
@login_required
def edit_recipe(recipes_id):
    the_recipe = db.recipes.find_one({'_id': ObjectId(recipes_id)})
    # Check if user is the author of the recipe
    if the_recipe and the_recipe.get('author') != current_user.author:
        flash('You can only edit your own recipes')
        return redirect(url_for('get_recipes'))
    category_type = db.categories.find()
    cuisine = db.cuisines.find()
    difficulty = db.difficulty.find()
    return render_template('edit-recipe.html', recipes=the_recipe,
                    categories=category_type, cuisines=cuisine, difficulty=difficulty)
                           
# Update recipe
@app.route('/update_recipe/<recipes_id>', methods=["GET", "POST"])
@login_required
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
@login_required
def delete_recipe(recipes_id):
    recipe = db.recipes.find_one({'_id': ObjectId(recipes_id)})
    # Check if user is the author of the recipe
    if recipe and recipe.get('author') != current_user.author:
        flash('You can only delete your own recipes')
        return redirect(url_for('get_recipes'))
    db.recipes.delete_one({'_id': ObjectId(recipes_id)})
    flash('Recipe successfully deleted')
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
        print("Filtered results:", filtered_results)

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
        print("Filtered results:", filtered_results)
          
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

if __name__ == '__main__':
    app.run(
        host=os.environ.get('IP', '0.0.0.0'),
        port=int(os.environ.get('PORT', 5000)),
        debug=True
    )