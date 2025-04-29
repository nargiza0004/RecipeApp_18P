from flask import Flask, render_template, request, redirect, url_for, json
import os

app = Flask(__name__)


DB_FILE = 'recipes.json'


if not os.path.exists(DB_FILE):
    with open(DB_FILE, 'w') as f:
        json.dump([], f)

def get_recipes():
    with open(DB_FILE, 'r') as f:
        return json.load(f)

def save_recipes(recipes):
    with open(DB_FILE, 'w') as f:
        json.dump(recipes, f, indent=4)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/all_recipes')
def all_recipes():
    recipes = get_recipes()
    return render_template('all_recipes.html', recipes=recipes)


@app.route('/search_name', methods=['GET', 'POST'])
def search_name():
    if request.method == 'POST':
        query = request.form.get('recipe_name', '').lower()
        recipes = [r for r in get_recipes() if query in r['name'].lower()]
        return render_template('all_recipes.html', recipes=recipes)
    return render_template('search_name.html')

@app.route('/search_ingredients', methods=['GET', 'POST'])
def search_ingredients():
    if request.method == 'POST':
        query = request.form.get('ingredients', '').lower()
        recipes = []
        for recipe in get_recipes():
            ingredients = [i.strip().lower() for i in recipe['ingredients'].split(',')]
            if all(q.strip().lower() in ingredients for q in query.split(',')):
                recipes.append(recipe)
        return render_template('all_recipes.html', recipes=recipes)
    return render_template('search_ingredients.html')

@app.route('/add_recipe', methods=['GET', 'POST'])
def add_recipe():
    if request.method == 'POST':
        name = request.form.get('name')
        ingredients = request.form.get('ingredients')
        instructions = request.form.get('instructions')
        
        if name and ingredients and instructions:
            new_recipe = {
                'name': name,
                'ingredients': ingredients,
                'instructions': instructions
            }
            recipes = get_recipes()
            recipes.append(new_recipe)
            save_recipes(recipes)
            return redirect(url_for('all_recipes'))
    
    return render_template('add_recipe.html')

@app.route('/edit_recipe/<int:recipe_id>', methods=['GET', 'POST'])
def edit_recipe(recipe_id):
    recipes = get_recipes()
    recipe = recipes[recipe_id]
    
    if request.method == 'POST':
        recipe['name'] = request.form['name']
        recipe['ingredients'] = request.form['ingredients']
        recipe['instructions'] = request.form['instructions']
        save_recipes(recipes)
        return redirect(url_for('all_recipes'))
    
    return render_template('edit_recipe.html', recipe=recipe, recipe_id=recipe_id)

@app.route('/delete_recipe/<int:recipe_id>')
def delete_recipe(recipe_id):
    recipes = get_recipes()
    del recipes[recipe_id]
    save_recipes(recipes)
    return redirect(url_for('all_recipes'))

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)
