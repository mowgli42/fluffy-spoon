import os
from lxml import etree

import xml.etree.ElementTree as ET
import argparse

# Define paths (relative to this repo)
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, '..'))
xml_directory = os.path.join(PROJECT_DIR, 'recipes')
xsl_file = os.path.join(PROJECT_DIR, 'stylesheets', 'recipe-style.xsl')
output_directory = os.path.join(PROJECT_DIR, 'web', 'recipes')

THEMES = {
    'light': '#f8f9fa',
    'warm': '#fff7ed',
    'mint': '#ecfeff',
    'dark': '#0f172a',
}

PAGE_BG_TOKEN = '__PAGE_BACKGROUND__'

# Ensure output directory exists
os.makedirs(output_directory, exist_ok=True)

# Function to transform XML to HTML using XSLT
def transform_xml_to_html(xml_file):
    # Parse the XML and XSL files
    xml_tree = etree.parse(xml_file)
    xslt_tree = etree.parse(xsl_file)
    transform = etree.XSLT(xslt_tree)

    # Transform XML to HTML
    html_tree = transform(xml_tree)
    return str(html_tree)

# Function to generate recipe pages
def generate_recipe_pages(page_background: str):
    for xml_file in os.listdir(xml_directory):
        if xml_file.endswith('.xml'):
            xml_path = os.path.join(xml_directory, xml_file)
            html_content = transform_xml_to_html(xml_path)
            html_content = html_content.replace(PAGE_BG_TOKEN, page_background)

            # Create HTML file for each recipe
            recipe_name = os.path.splitext(xml_file)[0]
            output_file = os.path.join(output_directory, f'{recipe_name}.html')

            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(html_content)

            print(f'Generated: {output_file}')

# Main execution
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate recipe HTML pages from XML + XSLT')
    parser.add_argument(
        '--theme',
        choices=sorted(THEMES.keys()),
        default='light',
        help='Background theme for generated recipe pages',
    )
    parser.add_argument(
        '--page-background',
        default=None,
        help='Custom CSS background value (overrides --theme), e.g. "#111827" or "linear-gradient(...)"',
    )
    args = parser.parse_args()

    background = args.page_background if args.page_background else THEMES[args.theme]
    generate_recipe_pages(page_background=background)