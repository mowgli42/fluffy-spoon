#!/usr/bin/env python3
"""
Simple Recipe XML generator web app + CLI.

Usage:
  - CLI test (no Flask required):
      python recipe-web-generator.py --create-sample

  - Run web server (requires Flask, local dev only):
      cp .env.example .env   # set ENABLE_RECIPE_CREATE and FLASK_SECRET_KEY
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

    category = ET.SubElement(root, 'category')
    category.text = data.get('category', 'uncategorized')

    preparation_el = ET.SubElement(root, 'preparation')
    for idx, step in enumerate(data.get('steps', []), start=1):
        s = ET.SubElement(preparation_el, 'step')
        s.set('number', str(idx))
        s.text = step

    meta_created = ET.SubElement(root, 'created')
    meta_created.text = datetime.datetime.now(datetime.timezone.utc).isoformat().replace('+00:00', 'Z')

    return root


def safe_recipe_filename(filename):
    base = os.path.basename(filename)
    if base != filename or not re.fullmatch(r'[a-z0-9-]+\.xml', base):
        raise ValueError(f'Invalid recipe filename: {filename!r}')
    return base


def write_recipe_xml(elem, filename):
    filename = safe_recipe_filename(filename)
    path = os.path.join(RECIPES_DIR, filename)
    resolved = os.path.realpath(path)
    recipes_root = os.path.realpath(RECIPES_DIR)
    if not resolved.startswith(recipes_root + os.sep):
        raise ValueError('Recipe path escapes recipes directory')
    xml_bytes = prettify_xml(elem)
    with open(resolved, 'wb') as f:
        f.write(xml_bytes)
    return resolved


def create_sample_recipe():
    data = {
        'title': 'Sample Lemon Pasta',
        'summary': 'Bright lemon pasta with parmesan and herbs.',
        'servings': 2,
        'totalTime': '20 minutes',
        'difficulty': 'easy',
        'tags': ['pasta', 'quick', 'vegetarian'],
        'category': 'main-course',
        'ingredients': [
            '200g spaghetti',
            '1 lemon, zested and juiced',
            '2 tbsp butter',
            '50g parmesan, grated',
            'Salt and pepper to taste',
        ],
        'steps': [
            'Cook pasta according to package instructions.',
            'Reserve some pasta water.',
            'Combine lemon, butter, and cheese off heat.',
            'Toss pasta with sauce, adding pasta water to loosen.',
        ],
    }
    elem = build_recipe_element(data)
    base = slugify(data['title'])
    filename = f"{base}.xml"
    final_path = write_recipe_xml(elem, filename)
    print(f"Wrote sample recipe to: {final_path}")


def run_server(host='127.0.0.1', port=8000):
    try:
        from flask import (
            Flask,
            request,
            render_template_string,
            redirect,
            url_for,
            flash,
            abort,
            send_from_directory,
        )
    except Exception:
        print('Flask not installed. Install dependencies with: pip install -r requirements.txt')
        sys.exit(1)

    if os.environ.get('ENABLE_RECIPE_CREATE', '').lower() not in ('1', 'true', 'yes'):
        print(
            'Recipe creation server is disabled. Set ENABLE_RECIPE_CREATE=true for local development.'
        )
        sys.exit(1)

    secret = os.environ.get('FLASK_SECRET_KEY')
    if not secret:
        print('Set FLASK_SECRET_KEY before running the recipe creation server.')
        sys.exit(1)

    app = Flask(__name__)
    app.secret_key = secret
    app.config['MAX_CONTENT_LENGTH'] = 64 * 1024

    web_dir = os.path.abspath(os.path.join(SCRIPT_DIR, '..', 'web'))
    recipe_home_url = os.environ.get('RECIPE_HOME_URL', '/recipe-box')

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
        <label>Title<input name="title" required maxlength="200"></label>
        <label>Summary<textarea name="summary" rows="3" maxlength="2000"></textarea></label>
        <label>Servings<input name="servings" value="4" maxlength="10"></label>
        <label>Total Time<input name="totalTime" placeholder="e.g. 45 minutes" maxlength="100"></label>
        <label>Difficulty<select name="difficulty"><option>easy</option><option>medium</option><option>hard</option></select></label>
        <label>Tags (comma-separated)<input name="tags" maxlength="500"></label>
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
      <p style="margin-top:14px;font-size:0.95em;color:#444">After adding recipes locally, run <code>npm run generate</code> to rebuild the static site.</p>
      <p><a href="{{ recipe_home_url }}" style="display:inline-block;margin-top:8px;padding:8px 12px;background:#667eea;color:white;border-radius:8px;text-decoration:none">View Recipe Home</a></p>
    </body>
    </html>
    '''

    @app.route('/')
    def index():
        return render_template_string(FORM_HTML, recipe_home_url=recipe_home_url)

    @app.route('/recipe-box')
    def recipe_box():
        return send_from_directory(web_dir, 'recipe-box.html')

    @app.route('/create', methods=['POST'])
    def create():
        if host not in ('127.0.0.1', 'localhost', '::1'):
            abort(403)

        form = request.form
        title = (form.get('title') or '').strip()
        if not title or len(title) > 200:
            flash('Title is required and must be under 200 characters.')
            return redirect(url_for('index'))

        allowed_categories = {
            'uncategorized', 'breakfast', 'main-course', 'soup', 'dessert',
            'side-dish', 'salad', 'appetizer', 'beverage', 'snack', 'brunch',
        }
        category = (form.get('category') or 'uncategorized').strip()
        if category not in allowed_categories:
            category = 'uncategorized'

        difficulty = (form.get('difficulty') or 'medium').strip()
        if difficulty not in ('easy', 'medium', 'hard'):
            difficulty = 'medium'

        data = {
            'title': title,
            'summary': (form.get('summary') or '').strip()[:2000],
            'servings': (form.get('servings') or '4').strip()[:10],
            'totalTime': (form.get('totalTime') or '').strip()[:100],
            'difficulty': difficulty,
            'tags': [t.strip()[:50] for t in form.get('tags', '').split(',') if t.strip()][:20],
            'category': category,
            'ingredients': [
                line.strip()[:500]
                for line in form.get('ingredients', '').splitlines()
                if line.strip()
            ][:100],
            'steps': [
                line.strip()[:1000]
                for line in form.get('steps', '').splitlines()
                if line.strip()
            ][:50],
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
