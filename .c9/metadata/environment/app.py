{"changed":true,"filter":false,"title":"app.py","tooltip":"/app.py","value":"import os\nfrom flask import Flask, render_template, redirect, request, url_for\nfrom flask_pymongo import PyMongo\nfrom bson.objectid import ObjectId \n\napp = Flask(__name__)\napp.config[\"MONGO_DBNAME\"] = 'cook-book-db'\napp.config[\"MONGO_URI\"] = 'mongodb+srv://root:r00tUser@cluster2-6phdr.mongodb.net/cook-book-db?retryWrites=true&w=majority'\n\nmongo = PyMongo(app)\n\n\n@app.route('/')\n@app.route('/get_recipes')\ndef get_recipe():\n    return render_template(\"recipes.html\", recipes=mongo.db.recipes.find())\n    \n# Search box\n\n\n\n\n\n\n\n\n\n\nif __name__ == '__main__':\n    app.run(host=os.environ.get('IP'),\n            port=int(os.environ.get('PORT')),\n            debug=True)\n            \n","undoManager":{"mark":20,"position":19,"stack":[[{"start":{"row":0,"column":0},"end":{"row":14,"column":23},"action":"remove","lines":["import os","from flask import Flask","","app = Flask(__name__)","","","@app.route('/')","def hello():","    return 'Hello Cook Book!'","","","if __name__ == '__main__':","    app.run(host=os.environ.get('IP', '0.0.0.0'),","            port=int(os.environ.get('PORT', '5000')),","            debug=True)"],"id":2},{"start":{"row":0,"column":0},"end":{"row":21,"column":23},"action":"insert","lines":["import os","from flask import Flask, render_template, redirect, request, url_for","from flask_pymongo import PyMongo","from bson.objectid import ObjectId ","","app = Flask(__name__)","app.config[\"MONGO_DBNAME\"] = 'cook-book-db'","app.config[\"MONGO_URI\"] = 'mongodb+srv://root:r00tUser@cluster2-6phdr.mongodb.net/cook-book-db?retryWrites=true&w=majority'","","mongo = PyMongo(app)","","","@app.route('/')","@app.route('/get_recipe')","def get_recipe():","    return render_template(\"recipe.html\", recipe=mongo.db.recipe.find())","","","if __name__ == '__main__':","    app.run(host=os.environ.get('IP'),","            port=int(os.environ.get('PORT')),","            debug=True)"]}],[{"start":{"row":15,"column":34},"end":{"row":15,"column":35},"action":"insert","lines":["s"],"id":3}],[{"start":{"row":15,"column":65},"end":{"row":15,"column":66},"action":"insert","lines":["s"],"id":4}],[{"start":{"row":15,"column":49},"end":{"row":15,"column":50},"action":"insert","lines":["s"],"id":5}],[{"start":{"row":13,"column":23},"end":{"row":13,"column":24},"action":"insert","lines":["s"],"id":6}],[{"start":{"row":16,"column":0},"end":{"row":16,"column":4},"action":"insert","lines":["    "],"id":7}],[{"start":{"row":21,"column":23},"end":{"row":22,"column":0},"action":"insert","lines":["",""],"id":8},{"start":{"row":22,"column":0},"end":{"row":22,"column":12},"action":"insert","lines":["            "]}],[{"start":{"row":22,"column":8},"end":{"row":22,"column":12},"action":"remove","lines":["    "],"id":9},{"start":{"row":22,"column":4},"end":{"row":22,"column":8},"action":"remove","lines":["    "]},{"start":{"row":22,"column":0},"end":{"row":22,"column":4},"action":"remove","lines":["    "]},{"start":{"row":21,"column":23},"end":{"row":22,"column":0},"action":"remove","lines":["",""]}],[{"start":{"row":21,"column":23},"end":{"row":22,"column":0},"action":"insert","lines":["",""],"id":10},{"start":{"row":22,"column":0},"end":{"row":22,"column":12},"action":"insert","lines":["            "]},{"start":{"row":22,"column":12},"end":{"row":23,"column":0},"action":"insert","lines":["",""]},{"start":{"row":23,"column":0},"end":{"row":23,"column":12},"action":"insert","lines":["            "]}],[{"start":{"row":23,"column":8},"end":{"row":23,"column":12},"action":"remove","lines":["    "],"id":11},{"start":{"row":23,"column":4},"end":{"row":23,"column":8},"action":"remove","lines":["    "]},{"start":{"row":23,"column":0},"end":{"row":23,"column":4},"action":"remove","lines":["    "]}],[{"start":{"row":17,"column":0},"end":{"row":18,"column":0},"action":"insert","lines":["",""],"id":12},{"start":{"row":18,"column":0},"end":{"row":19,"column":0},"action":"insert","lines":["",""]},{"start":{"row":19,"column":0},"end":{"row":20,"column":0},"action":"insert","lines":["",""]},{"start":{"row":20,"column":0},"end":{"row":21,"column":0},"action":"insert","lines":["",""]},{"start":{"row":21,"column":0},"end":{"row":22,"column":0},"action":"insert","lines":["",""]},{"start":{"row":22,"column":0},"end":{"row":23,"column":0},"action":"insert","lines":["",""]},{"start":{"row":23,"column":0},"end":{"row":24,"column":0},"action":"insert","lines":["",""]},{"start":{"row":24,"column":0},"end":{"row":25,"column":0},"action":"insert","lines":["",""]}],[{"start":{"row":17,"column":0},"end":{"row":17,"column":1},"action":"insert","lines":["F"],"id":13},{"start":{"row":17,"column":1},"end":{"row":17,"column":2},"action":"insert","lines":["i"]},{"start":{"row":17,"column":2},"end":{"row":17,"column":3},"action":"insert","lines":["l"]},{"start":{"row":17,"column":3},"end":{"row":17,"column":4},"action":"insert","lines":["t"]},{"start":{"row":17,"column":4},"end":{"row":17,"column":5},"action":"insert","lines":["r"]},{"start":{"row":17,"column":5},"end":{"row":17,"column":6},"action":"insert","lines":["o"]}],[{"start":{"row":17,"column":0},"end":{"row":17,"column":2},"action":"insert","lines":["# "],"id":14}],[{"start":{"row":17,"column":8},"end":{"row":18,"column":0},"action":"insert","lines":["",""],"id":15}],[{"start":{"row":17,"column":2},"end":{"row":17,"column":8},"action":"remove","lines":["Filtro"],"id":16},{"start":{"row":17,"column":2},"end":{"row":17,"column":3},"action":"insert","lines":["S"]},{"start":{"row":17,"column":3},"end":{"row":17,"column":4},"action":"insert","lines":["e"]},{"start":{"row":17,"column":4},"end":{"row":17,"column":5},"action":"insert","lines":["a"]},{"start":{"row":17,"column":5},"end":{"row":17,"column":6},"action":"insert","lines":["r"]},{"start":{"row":17,"column":6},"end":{"row":17,"column":7},"action":"insert","lines":["c"]}],[{"start":{"row":17,"column":7},"end":{"row":17,"column":8},"action":"insert","lines":["h"],"id":17}],[{"start":{"row":17,"column":8},"end":{"row":17,"column":9},"action":"insert","lines":[" "],"id":18},{"start":{"row":17,"column":9},"end":{"row":17,"column":10},"action":"insert","lines":["b"]},{"start":{"row":17,"column":10},"end":{"row":17,"column":11},"action":"insert","lines":["i"]}],[{"start":{"row":17,"column":10},"end":{"row":17,"column":11},"action":"remove","lines":["i"],"id":19}],[{"start":{"row":17,"column":10},"end":{"row":17,"column":11},"action":"insert","lines":["o"],"id":20},{"start":{"row":17,"column":11},"end":{"row":17,"column":12},"action":"insert","lines":["x"]}],[{"start":{"row":17,"column":12},"end":{"row":18,"column":0},"action":"insert","lines":["",""],"id":21}],[{"start":{"row":18,"column":0},"end":{"row":49,"column":85},"action":"insert","lines":["\"\"\" Search by keyword \"\"\"","@app.route('/search_keyword', methods=['POST'])","def insert_keyword():","    return redirect(url_for('search_keyword', num=1, keyword=request.form.get('keyword')) ) ","    ","    ","@app.route('/search_keyword/<keyword>/page:<num>')","def search_keyword(keyword, num):","    recipes.create_index([","         (\"recipe_title\", \"text\"),","         (\"recipe_ingredients\", \"text\"),","         (\"cuisine_name\", \"text\"),","         (\"dish_type\", \"text\"),","         (\"recipe_author_name\", \"text\")","       ])","    keyword_result = recipes.find({\"$text\": ","        {\"$search\": keyword}}).sort([(\"upvotes\", -1)])","    keyword_count = keyword_result.count()","    total_pages = range(1, math.ceil(keyword_count/8) + 1)","    skip_num = 8 * (int(num)-1)","    recipes_per_page = keyword_result.skip(skip_num).limit(8)","    ","    if keyword_count <= 8:","        page_count = keyword_count","    elif (skip_num + 8) <= keyword_count:","        page_count = skip_num + 8","    else:","        page_count = keyword_count","    return render_template('searchkeyword.html', total_pages=total_pages, num=num, ","            keyword=keyword, recipes_per_page=recipes_per_page, skip_num=skip_num, ","            page_count=page_count, count=keyword_count, dishes=dishes.find(), ","            cuisines=cuisines.find(), users=users.find(), allergens=allergens.find())"],"id":22}]]},"ace":{"folds":[],"scrolltop":86,"scrollleft":0,"selection":{"start":{"row":13,"column":26},"end":{"row":13,"column":26},"isBackwards":false},"options":{"guessTabSize":true,"useWrapMode":false,"wrapToView":true},"firstLineState":{"row":30,"state":"start","mode":"ace/mode/python"}},"timestamp":1563643556258}