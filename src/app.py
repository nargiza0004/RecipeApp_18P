from flask import Flask, render_template, request, redirect, url_for, json
import os

app = Flask(__name__)

DB_FILE = 'recipes.json' # Our recipe file

if not os.path.exists(DB_FILE):
    with open(DB_FILE, 'w') as f:
        json.dump([], f)

def get_recipes(): #Grab all recipes from file
    with open(DB_FILE, 'r') as f:
        return json.load(f)

def save_recipes(recipes): #Save recipes to file
    with open(DB_FILE, 'w') as f:
        json.dump(recipes, f, indent=4)

@app.route('/') #home page
def index():
    return render_template('index.html')

@app.route('/all_recipes') #all recipes we have
def all_recipes():
    recipes = get_recipes()
    return render_template('all_recipes.html', recipes=recipes)


@app.route('/search_name', methods=['GET', 'POST']) #Search recipes by name
def search_name():
    if request.method == 'POST':
        query = request.form.get('recipe_name', '').lower()
        recipes = [r for r in get_recipes() if query in r['name'].lower()]
        return render_template('all_recipes.html', recipes=recipes)
    return render_template('search_name.html')

@app.route('/search_ingredients', methods=['GET', 'POST'])
def search_ingredients():
    if request.method == 'POST':
        query = request.form.get('ingredients', '').lower().strip()
        if not query:
            return render_template('search_ingredients.html', error="Please enter ingredients")

        recipes = get_recipes()
        found_recipes = []
        
        search_terms = []
        for term in query.split(','):
            search_terms.extend(term.strip().split())
        
        for recipe in recipes:
            recipe_ingredients = []
            for ing in recipe['ingredients'].split(','):
                recipe_ingredients.extend(ing.strip().lower().split())
            
            if any(term in recipe_ingredients for term in search_terms):
                found_recipes.append(recipe)
        
        return render_template('all_recipes.html', recipes=found_recipes)
    
    return render_template('search_ingredients.html')


@app.route('/add_recipe', methods=['GET', 'POST']) #new recipe
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

@app.route('/edit_recipe/<int:recipe_id>', methods=['GET', 'POST']) #edit recipe
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

@app.route('/delete_recipe/<int:recipe_id>') #delete recipe
def delete_recipe(recipe_id):
    recipes = get_recipes()
    del recipes[recipe_id]
    save_recipes(recipes)
    return redirect(url_for('all_recipes'))

@app.route('/about') #abut
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)
