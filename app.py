import os
from flask import Flask, render_template, request, redirect, url_for
from flask_pymongo import PyMongo, DESCENDING
from bson.objectid import ObjectId

app = Flask(__name__,
            template_folder='templates')
app.config['MONGO_DBNAME'] = 'sugar_app'
app.config['MONGO_URI'] = os.getenv('MONGO_URI')

mongo = PyMongo(app)

@app.route("/")
def home():
    return render_template('home.html', foods=mongo.db.foods.find())

@app.route('/get_foods')
def get_foods():
    return render_template('foods.html', foods=mongo.db.foods.find())

# @app.route('/get_drinks')
# def get_drink():
#     return render_template('drinks.html', drinks=mongo.db.drinks.find())

@app.route('/add_food')
def add_food():
    food_groups = mongo.db.food_group.find()
    return render_template('addfood.html', food_groups=food_groups)

# @app.route('/add_drink')
# def add_drink():
#     return render_template('adddrink.html', categories=mongo.db.drink_categories.find())

@app.route('/insert_food', methods=['POST'])
def insert_food():
    foods_collection = mongo.db.foods
    food = request.form.to_dict()
    food.pop('action')
    food['sugar_g_per_100g'] = float(food['sugar_g_per_100g'])
    food['sugar_g_per_serving'] = float(food['sugar_g_per_serving'])
    food['reviewed'] = False
    foods_collection.insert_one(food)
    return redirect(url_for('get_foods'))

@app.route('/edit_food/<food_id>')
def edit_food(food_id):
    food = mongo.db.foods.find_one({'_id': ObjectId(food_id)})
    food_groups = mongo.db.food_group.find()
    return render_template('editfood.html', food=food, food_groups=food_groups)

@app.route('/update_food/<food_id>', methods=['POST'])
def update_food(food_id):
    foods_collection = mongo.db.foods
    foods_collection.update_one({'_id': ObjectId(food_id)},
                     {'$set':
                      {
                          'name': request.form.get('food_name'),
                          'group': request.form.get('food_group'),
                          'sugar_g_per_100g': float(request.form.get('sugar_g_per_100g')),
                          'sugar_g_per_serving': float(request.form.get('sugar_g_per_serving')),
                          'serving_description': request.form.get('serving_description'),
                          'reviewed': (request.form.get('reviewed') == "on"),
                      }
                      })
    return redirect(url_for('get_foods'))

@app.route('/dbstats')
def get_dbstats():
    return "<h1>DB Stats</h1>"

@app.route('/sort/<int:sort_id>')
def sort(sort_id):
    html = ""
    if sort_id == 1:
        html = "<h1>Sort id is Sugar: High to Low</h1>"
    elif sort_id == 2:
        html = "<h1>Sort id is Sugar: Low to High</h1>"
    elif sort_id == 3:
        html = "<h1>Sort id is A - Z</h1>"
    elif sort_id == 4:
        html = "<h1>Sort id is Z - A</h1>"
    else:
        html = "<h1>Error</h1>"

    return html

@app.route('/apply_filters', methods=['POST'])
def apply_filters():
    category = request.form.get('category')
    if category == 'food':
        victuals = mongo.db.foods.find()
    else:
        victuals = mongo.db.drinks.find()
    
    sugar_measure = request.form.get('sugar-measure')
    sort_by = request.form.get('sort-by')

    if (sort_by == 'H-L') or (sort_by == 'L-H'):
        if sugar_measure == 'serving':
            if sort_by == 'H-L':
                victuals_sorted = victuals.sort("sugar_g_per_serving", DESCENDING)
            else:
                victuals_sorted = victuals.sort("sugar_g_per_serving")
        elif sugar_measure == '100g':
            if sort_by == 'H-L':
                victuals_sorted = victuals.sort("sugar_g_per_100g", DESCENDING)
            else:
                victuals_sorted = victuals.sort("sugar_g_per_100g")
        elif sugar_measure == '100ml':
            if sort_by == 'H-L':
                victuals_sorted = victuals.sort("sugar_g_per_100ml", DESCENDING)
            else:
                victuals_sorted = victuals.sort("sugar_g_per_100ml")
    elif sort_by == 'A-Z':
        victuals_sorted = victuals.sort("name")
    elif sort_by == 'Z-A':
        victuals_sorted = victuals.sort("name", DESCENDING)
    else:
        victuals_sorted = victuals.sort("name")

    # return the html get_foods ?
    # send in victuals_sorted as foods, category, sort_by and sugar_measure (so as to set defaults fo filters)
    return "<h1>Category {0}, Sugar Per {1}, Sort by {2}</h1>".format(html0,html1, html2)

if __name__ == '__main__':
    #app.run(host=os.environ.get('IP'),
    #        port=int(os.environ.get('PORT')),
    #        debug=False)
    app.run(debug=True)