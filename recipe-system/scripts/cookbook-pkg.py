import os
import json
import urllib.request
import urllib.error
from lxml import etree

# Load XSD schema for validation
SCHEMA = None
try:
    schema_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'schemas', 'recipe.xsd'))
    schema_doc = etree.parse(schema_path)
    SCHEMA = etree.XMLSchema(schema_doc)
except Exception as _e:
    SCHEMA = None

# filepath: /home/tprettol/repo/fluffy-spoon/recipe-system/scripts/cookbook-pkg.py

# Define paths
xml_directory = '/home/tprettol/repo/fluffy-spoon/recipe-system/recipes'
output_directory = '/home/tprettol/repo/fluffy-spoon/recipe-system/web/recipes'
cookbook_output = '/home/tprettol/repo/fluffy-spoon/recipe-system/web/recipe-box.html'

def extract_recipe_metadata(xml_file):
    """Extract metadata from XML recipe file"""
    try:
        tree = etree.parse(xml_file)
        root = tree.getroot()
        
        # Define namespace
        ns = {'r': 'http://www.example.com/recipe'}
        
        # Extract basic info - use namespace prefix for XPath queries
        title = root.findtext('.//r:title', 'Unknown Recipe', ns)
        summary = root.findtext('.//r:description/r:summary', '', ns)
        servings = root.findtext('.//r:metadata/r:servings', '4', ns)
        totalTime = root.findtext('.//r:metadata/r:totalTime', '0 minutes', ns)
        difficulty = root.findtext('.//r:metadata/r:difficulty', 'medium', ns)
        
        # Extract tags/categories
        tags = [tag.text for tag in root.findall('.//r:tag', ns) if tag.text]
        category = root.findtext('.//r:category', 'uncategorized', ns)
        
        # Parse totalTime to minutes for filtering
        totalTimeMinutes = parse_time_to_minutes(totalTime)

        # Validate against XSD if available
        valid = True
        validation_errors = []
        if SCHEMA is not None:
            try:
                valid = SCHEMA.validate(tree)
                if not valid:
                    validation_errors = [str(err) for err in SCHEMA.error_log]
            except Exception as e:
                valid = False
                validation_errors = [str(e)]

        return {
            'title': title,
            'description': summary,
            'servings': int(servings) if servings.isdigit() else 4,
            'totalTime': totalTimeMinutes,
            'totalTimeDisplay': totalTime,
            'difficulty': difficulty,
            'tags': tags,
            'category': category
            , 'valid': valid,
            'validationErrors': validation_errors
        }
    except Exception as e:
        print(f"Error parsing {xml_file}: {e}")
        return None

def parse_time_to_minutes(time_str):
    """Convert time string like '1 hour 45 minutes' to total minutes"""
    time_str = time_str.lower().strip()
    total_minutes = 0
    
    # Handle hours
    if 'hour' in time_str:
        parts = time_str.split('hour')
        hours = int(''.join(filter(str.isdigit, parts[0].strip())))
        total_minutes += hours * 60
    
    # Handle minutes
    if 'minute' in time_str:
        # Extract the number before 'minute'
        parts = time_str.split('minute')
        remaining = parts[0].strip()
        # Get the last number in the remaining string
        numbers = ''.join(filter(lambda x: x.isdigit() or x == ' ', remaining)).split()
        if numbers:
            minutes = int(numbers[-1])
            total_minutes += minutes
    
    return total_minutes if total_minutes > 0 else 0

def generate_recipe_box():
    """Generate recipe-box.html with all recipes"""
    recipes = []
    
    # Scan XML directory for recipe files
    for filename in os.listdir(xml_directory):
        if filename.endswith('.xml'):
            xml_path = os.path.join(xml_directory, filename)
            metadata = extract_recipe_metadata(xml_path)
            
            if metadata:
                recipe_name = os.path.splitext(filename)[0]
                metadata['id'] = recipe_name
                metadata['path'] = f'recipes/{recipe_name}.html'
                recipes.append(metadata)
    
    # Check whether the recipe generator server is reachable (can be overridden)
    server_url = os.environ.get('RECIPE_GENERATOR_URL', 'http://127.0.0.1:8000/')
    def server_is_up(url):
        try:
            req = urllib.request.Request(url, method='HEAD')
            with urllib.request.urlopen(req, timeout=1) as resp:
                return getattr(resp, 'status', 200) < 400
        except Exception:
            return False

    create_link_html = ''
    if server_is_up(server_url):
        create_link_html = f'<a class="create-btn" href="{server_url}" target="_blank" rel="noopener">＋ Create Recipe</a>'

    # Generate HTML with embedded recipe data
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Recipe Collection - Search & Browse</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }}

        .container {{
            max-width: 1400px;
            margin: 0 auto;
        }}

        header {{
            text-align: center;
            color: white;
            margin-bottom: 40px;
        }}

        h1 {{
            font-size: 3em;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }}

        .subtitle {{
            font-size: 1.2em;
            opacity: 0.9;
        }}

        .create-btn {{
            display: inline-block;
            margin-top: 12px;
            padding: 8px 12px;
            background: white;
            color: #667eea;
            border-radius: 8px;
            font-weight: 600;
            text-decoration: none;
            box-shadow: 0 6px 18px rgba(0,0,0,0.12);
        }}

        .create-btn:hover {{
            transform: translateY(-2px);
            box-shadow: 0 10px 25px rgba(0,0,0,0.15);
        }}

        .footer-section {{
            text-align: center;
            margin-top: 40px;
            padding: 30px 0;
        }}

        .search-section {{
            background: white;
            border-radius: 15px;
            padding: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
            margin-bottom: 30px;
        }}

        .search-bar {{
            display: flex;
            gap: 10px;
            margin-bottom: 20px;
        }}

        .search-input {{
            flex: 1;
            padding: 15px 20px;
            font-size: 1.1em;
            border: 2px solid #e0e0e0;
            border-radius: 10px;
            transition: border-color 0.3s;
        }}

        .search-input:focus {{
            outline: none;
            border-color: #667eea;
        }}

        .search-btn {{
            padding: 15px 40px;
            font-size: 1.1em;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 10px;
            cursor: pointer;
            font-weight: bold;
            transition: transform 0.2s;
        }}

        .search-btn:hover {{
            transform: scale(1.05);
        }}

        .filters {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 15px;
        }}

        .filter-group {{
            background: #f8f9fa;
            padding: 15px;
            border-radius: 10px;
        }}

        .filter-group h3 {{
            font-size: 0.9em;
            color: #666;
            margin-bottom: 10px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}

        .tag-container {{
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
        }}

        .tag {{
            padding: 6px 12px;
            border-radius: 20px;
            font-size: 0.9em;
            cursor: pointer;
            transition: all 0.3s;
            background: white;
            border: 2px solid #e0e0e0;
        }}

        .tag:hover {{
            border-color: #667eea;
            transform: translateY(-2px);
        }}

        .tag.active {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-color: transparent;
        }}

        .results-section {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
            gap: 25px;
        }}

        .recipe-card {{
            background: white;
            border-radius: 15px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
            transition: transform 0.3s, box-shadow 0.3s;
            cursor: pointer;
        }}

        .recipe-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 10px 25px rgba(0,0,0,0.3);
        }}


        .recipe-content {{
                padding: 15px;
        }}

        .recipe-title {{
                font-size: 1.2em;
            color: #333;
                margin-bottom: 8px;
            font-weight: bold;
        }}

        .recipe-meta {{
            display: flex;
            gap: 15px;
                margin: 8px 0;
            flex-wrap: wrap;
        }}

        .meta-item {{
            display: flex;
            align-items: center;
            gap: 5px;
                font-size: 0.85em;
            color: #666;
        }}

        .recipe-tags {{
            display: flex;
            flex-wrap: wrap;
            gap: 6px;
                margin-bottom: 8px;
        }}

        .recipe-tag {{
            padding: 4px 10px;
                background: #e8ebff;
                color: #667eea;
            border-radius: 15px;
            font-size: 0.8em;
        }}

        .stats {{
            display: flex;
            justify-content: space-around;
            background: white;
            border-radius: 15px;
            padding: 20px;
            margin-bottom: 30px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        }}

        .stat-item {{
            text-align: center;
        }}

        .stat-number {{
            font-size: 2em;
            font-weight: bold;
            color: #667eea;
        }}

        .stat-label {{
            color: #666;
            font-size: 0.9em;
            margin-top: 5px;
        }}

        .no-results {{
            grid-column: 1 / -1;
            text-align: center;
            padding: 60px;
            background: white;
            border-radius: 15px;
            color: #666;
            font-size: 1.2em;
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🍳 My Recipe Collection</h1>
            <p class="subtitle">Search and browse your personal recipe library</p>
        </header>

        <div class="stats">
        <div class="search-section">
            <div class="search-bar">
                <input type="text" class="search-input" id="searchInput" placeholder="Search recipes by name, ingredient, or description...">
                <button class="search-btn" onclick="searchRecipes()">Search</button>
            </div>

            <div class="filters">
                <div class="filter-group">
                    <h3>Difficulty</h3>
                    <div class="tag-container" id="difficultyFilter">
                        <span class="tag" data-filter="easy">Easy</span>
                        <span class="tag" data-filter="medium">Medium</span>
                        <span class="tag" data-filter="hard">Hard</span>
                    </div>
                </div>

                <div class="filter-group">
                    <h3>Cooking Time</h3>
                    <div class="tag-container" id="timeFilter">
                        <span class="tag" data-filter="quick">Under 30 min</span>
                        <span class="tag" data-filter="medium">30-60 min</span>
                        <span class="tag" data-filter="long">Over 1 hour</span>
                    </div>
                </div>
            </div>
        </div>

        <div class="results-section" id="results">
            <!-- Recipe cards generated by JavaScript -->
        </div>

        <div class="footer-section">
            {create_link_html}
        </div>
    </div>

    <script>
        const recipes = {json.dumps(recipes)};

        let activeFilters = new Set();
        let currentRecipes = recipes;

        function initializeFilters() {{
            document.querySelectorAll('.tag').forEach(tag => {{
                tag.addEventListener('click', function() {{
                    const filter = this.dataset.filter;
                    
                    if (this.classList.contains('active')) {{
                        this.classList.remove('active');
                        activeFilters.delete(filter);
                    }} else {{
                        this.classList.add('active');
                        activeFilters.add(filter);
                    }}
                    
                    filterRecipes();
                }});
            }});
        }}

        function updateStats() {{
            const allTags = new Set();
            const allCategories = new Set();
            
            recipes.forEach(recipe => {{
                recipe.tags.forEach(tag => allTags.add(tag));
                allCategories.add(recipe.category);
            }});
            
            const totalTagsEl = document.getElementById('totalTags');
            const categoriesEl = document.getElementById('categories');
            if (totalTagsEl) totalTagsEl.textContent = allTags.size;
            if (categoriesEl) categoriesEl.textContent = allCategories.size;
        }}

        function filterRecipes() {{
            const searchTerm = document.getElementById('searchInput').value.toLowerCase();
            
            currentRecipes = recipes.filter(recipe => {{
                const matchesSearch = !searchTerm || 
                    recipe.title.toLowerCase().includes(searchTerm) ||
                    recipe.description.toLowerCase().includes(searchTerm) ||
                    recipe.tags.some(tag => tag.toLowerCase().includes(searchTerm));
                
                const matchesFilters = activeFilters.size === 0 ||
                    Array.from(activeFilters).some(filter => {{
                        if (filter === 'quick') return recipe.totalTime <= 30;
                        if (filter === 'medium') return recipe.totalTime > 30 && recipe.totalTime <= 60;
                        if (filter === 'long') return recipe.totalTime > 60;
                        return recipe.difficulty === filter;
                    }});
                
                return matchesSearch && matchesFilters;
            }});
            
            displayRecipes();
        }}

        function displayRecipes() {{
            const resultsContainer = document.getElementById('results');
            
            if (currentRecipes.length === 0) {{
                resultsContainer.innerHTML = '<div class="no-results">No recipes found. Try adjusting your search or filters.</div>';
                return;
            }}
            
            resultsContainer.innerHTML = currentRecipes.map(recipe => `
                <div class="recipe-card" onclick="openRecipe('${{recipe.path}}')">
                    <div class="recipe-content">
                            <div class="recipe-tags">
                                ${{recipe.tags.slice(0, 3).map(tag => `<span class="recipe-tag">${{tag}}</span>`).join('')}}
                            </div>
                        <div class="recipe-title">${{recipe.title}}</div>
                        <div class="recipe-meta">
                            <span class="meta-item">⏱️ ${{recipe.totalTimeDisplay}}</span>
                            <span class="meta-item">📊 ${{recipe.difficulty}}</span>
                            ${{recipe.valid ? '' : `<span class="meta-item" title="${{recipe.validationErrors.join(' | ')}}" style="color:#d32f2f">⚠️ Invalid</span>`}}
                        </div>
                            <p style="color: #666; font-size: 0.9em; margin-top: 8px; line-height: 1.4;">${{recipe.description.substring(0, 120)}}...</p>
                    </div>
                </div>
            `).join('');
        }}

        function searchRecipes() {{
            filterRecipes();
        }}

        function openRecipe(path) {{
            window.location.href = path;
        }}

        document.getElementById('searchInput').addEventListener('input', filterRecipes);

        initializeFilters();
        updateStats();
        displayRecipes();
    </script>
</body>
</html>
"""
    
    # Write the HTML file
    with open(cookbook_output, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f'Generated recipe-box.html with {len(recipes)} recipes at {cookbook_output}')

if __name__ == '__main__':
    generate_recipe_box()