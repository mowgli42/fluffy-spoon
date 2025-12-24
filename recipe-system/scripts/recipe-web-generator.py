#!/usr/bin/env python3
"""
Simple Recipe XML generator web app + CLI.

Usage:
  - CLI test (no Flask required):
      python recipe-web-generator.py --create-sample

  - Run web server (requires Flask):
      pip install -r requirements.txt
      python recipe-web-generator.py --serve

The web UI provides a form to create a recipe XML file placed in the recipes folder.
"""
import os
import argparse
import datetime
import re
import sys
from xml.etree import ElementTree as ET
from xml.dom import minidom

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
RECIPES_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, '..', 'recipes'))
NS = 'http://www.example.com/recipe'

os.makedirs(RECIPES_DIR, exist_ok=True)


def slugify(text):
    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9]+", '-', text)
    text = re.sub(r"-+", '-', text).strip('-')
    return text or 'recipe'


def prettify_xml(elem):
    rough = ET.tostring(elem, encoding='utf-8')
    parsed = minidom.parseString(rough)
    return parsed.toprettyxml(indent='  ', encoding='utf-8')


def build_recipe_element(data):
    # Create root with default namespace
    root = ET.Element('recipe', xmlns=NS)

    title = ET.SubElement(root, 'title')
    title.text = data.get('title', 'Untitled Recipe')

    description = ET.SubElement(root, 'description')
    summary = ET.SubElement(description, 'summary')
    summary.text = data.get('summary', '')

    metadata = ET.SubElement(root, 'metadata')
    servings = ET.SubElement(metadata, 'servings')
    servings.text = str(data.get('servings', '4'))
    totalTime = ET.SubElement(metadata, 'totalTime')
    totalTime.text = data.get('totalTime', '')
    difficulty = ET.SubElement(metadata, 'difficulty')
    difficulty.text = data.get('difficulty', 'medium')

    # Schema expects tags inside description/tags/tag
    tags = data.get('tags', [])
    if tags:
        tags_el = ET.SubElement(description, 'tags')
        for t in tags:
            tag_el = ET.SubElement(tags_el, 'tag')
            tag_el.text = t

    ingredients_el = ET.SubElement(root, 'ingredients')
    for ing in data.get('ingredients', []):
        i = ET.SubElement(ingredients_el, 'ingredient')
        i.text = ing

    # include top-level category element for cookbook indexing (placed before preparation per schema)
    category = ET.SubElement(root, 'category')
    category.text = data.get('category', 'uncategorized')

    preparation_el = ET.SubElement(root, 'preparation')
    for idx, step in enumerate(data.get('steps', []), start=1):
        s = ET.SubElement(preparation_el, 'step')
        s.set('number', str(idx))
        s.text = step

    # Optionally add created timestamp
    meta_created = ET.SubElement(root, 'created')
    meta_created.text = datetime.datetime.utcnow().isoformat() + 'Z'

    return root


def write_recipe_xml(elem, filename):
    path = os.path.join(RECIPES_DIR, filename)
    xml_bytes = prettify_xml(elem)
    with open(path, 'wb') as f:
        f.write(xml_bytes)
    return path


def create_sample_recipe():
    data = {
        'title': 'Sample Lemon Pasta',
        'summary': 'Bright lemon pasta with parmesan and herbs.',
        'servings': 2,
        'totalTime': '20 minutes',
        'difficulty': 'easy',
        'tags': ['pasta', 'quick', 'vegetarian'],
        'category': 'main-course',
        'ingredients': ['200g spaghetti', '1 lemon, zested and juiced', '2 tbsp butter', '50g parmesan, grated', 'Salt and pepper to taste'],
        'steps': ['Cook pasta according to package instructions.', 'Reserve some pasta water.', 'Combine lemon, butter, and cheese off heat.', 'Toss pasta with sauce, adding pasta water to loosen.']
    }
    elem = build_recipe_element(data)
    base = slugify(data['title'])
    filename = f"{base}.xml"
    final_path = write_recipe_xml(elem, filename)
    print(f"Wrote sample recipe to: {final_path}")


# --- Minimal Flask app when requested ---

def run_server(host='127.0.0.1', port=8000):
    try:
        from flask import Flask, request, render_template_string, redirect, url_for, flash
    except Exception:
        print('Flask not installed. Install dependencies with: pip install -r requirements.txt')
        sys.exit(1)

    app = Flask(__name__)
    app.secret_key = 'dev-secret'

    # compute file URL for the generated recipe homepage
    recipe_box_path = os.path.abspath(os.path.join(SCRIPT_DIR, '..', 'web', 'recipe-box.html'))
    recipe_home_url = 'file://' + recipe_box_path

    FORM_HTML = '''
    <!doctype html>
    <html>
    <head>
      <meta charset="utf-8">
      <title>Create Recipe</title>
      <style>body{font-family:Arial,Helvetica,sans-serif;padding:20px}label{display:block;margin-top:8px}input,textarea,select{width:100%;padding:8px;margin-top:4px}</style>
    </head>
    <body>
      <h1>Create Recipe XML</h1>
      {% with messages = get_flashed_messages() %}
        {% if messages %}
          <ul style="color:green">{% for m in messages %}<li>{{m}}</li>{% endfor %}</ul>
        {% endif %}
      {% endwith %}
      <form method="post" action="/create">
        <label>Title<input name="title" required></label>
        <label>Summary<textarea name="summary" rows="3"></textarea></label>
        <label>Servings<input name="servings" value="4"></label>
        <label>Total Time<input name="totalTime" placeholder="e.g. 45 minutes"></label>
        <label>Difficulty<select name="difficulty"><option>easy</option><option>medium</option><option>hard</option></select></label>
                <label>Tags (comma-separated)<input name="tags"></label>
                <label>Category
                    <select name="category">
                        <option value="uncategorized">Uncategorized</option>
                        <option value="breakfast">Breakfast</option>
                        <option value="main-course">Main Course</option>
                        <option value="soup">Soup</option>
                        <option value="dessert">Dessert</option>
                        <option value="side-dish">Side Dish</option>
                        <option value="salad">Salad</option>
                        <option value="appetizer">Appetizer</option>
                        <option value="beverage">Beverage</option>
                        <option value="snack">Snack</option>
                        <option value="brunch">Brunch</option>
                    </select>
                </label>
        <label>Ingredients (one per line)<textarea name="ingredients" rows="5"></textarea></label>
        <label>Steps (one per line)<textarea name="steps" rows="6"></textarea></label>
        <button type="submit" style="margin-top:12px;padding:10px 16px">Create</button>
      </form>
            <p style="margin-top:14px;font-size:0.95em;color:#444">Once you've added recipes, re-run <code>recipe-gen.py</code> and <code>cookbook-pkg.py</code> to regenerate the site.</p>
            <p><a href="#" id="viewHome" style="display:inline-block;margin-top:8px;padding:8px 12px;background:#667eea;color:white;border-radius:8px;text-decoration:none">View Recipe Home</a></p>
            <script>
                document.getElementById('viewHome').addEventListener('click', function(e){
                    e.preventDefault();
                    if (confirm('To see newly created recipes you must re-run recipe-gen.py and cookbook-pkg.py. Open the recipe homepage now?')) {
                        window.open('{{ recipe_home_url }}', '_blank');
                    }
                });
            </script>
    </body>
    </html>
    '''

    @app.route('/')
    def index():
        return render_template_string(FORM_HTML, recipe_home_url=recipe_home_url)

    @app.route('/create', methods=['POST'])
    def create():
        form = request.form
        title = form.get('title').strip()
        data = {
            'title': title,
            'summary': form.get('summary','').strip(),
            'servings': form.get('servings','4').strip(),
            'totalTime': form.get('totalTime','').strip(),
            'difficulty': form.get('difficulty','medium').strip(),
            'tags': [t.strip() for t in form.get('tags','').split(',') if t.strip()],
            'category': form.get('category','uncategorized').strip(),
            'ingredients': [l.strip() for l in form.get('ingredients','').splitlines() if l.strip()],
            'steps': [l.strip() for l in form.get('steps','').splitlines() if l.strip()]
        }
        elem = build_recipe_element(data)
        base = slugify(title)
        filename = f"{base}.xml"
        final_path = write_recipe_xml(elem, filename)
        flash(f'Wrote recipe: {os.path.basename(final_path)}')
        return redirect(url_for('index'))

    print(f"Starting server on http://{host}:{port} — recipes dir: {RECIPES_DIR}")
    app.run(host=host, port=port)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Recipe XML generator web app + CLI')
    parser.add_argument('--create-sample', action='store_true', help='Create a sample recipe XML in recipes folder and exit')
    parser.add_argument('--serve', action='store_true', help='Run simple Flask server for creating recipes')
    parser.add_argument('--host', default='127.0.0.1')
    parser.add_argument('--port', default=8000, type=int)
    args = parser.parse_args()

    if args.create_sample:
        create_sample_recipe()
        sys.exit(0)

    if args.serve:
        run_server(host=args.host, port=args.port)
        sys.exit(0)

    parser.print_help()
