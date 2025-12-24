import os
from lxml import etree

import xml.etree.ElementTree as ET

# Define paths
xml_directory = '/home/tprettol/repo/cookbook-lite/recipe-system/recipes'  # Update with the actual path to your XML files
xsl_file = '/home/tprettol/repo/cookbook-lite/recipe-system/stylesheets/recipe-style.xsl'
output_directory = '/home/tprettol/repo/cookbook-lite/recipe-system/web/recipes'

# Ensure output directory exists
os.makedirs(output_directory, exist_ok=True)

# Function to transform XML to HTML using XSLT
def transform_xml_to_html(xml_file):
    # Parse the XML and XSL files
    xml_tree = ET.parse(xml_file)
    xslt_tree = etree.parse(xsl_file)
    transform = etree.XSLT(xslt_tree)

    # Transform XML to HTML
    html_tree = transform(xml_tree)
    return str(html_tree)

# Function to generate recipe pages
def generate_recipe_pages():
    for xml_file in os.listdir(xml_directory):
        if xml_file.endswith('.xml'):
            xml_path = os.path.join(xml_directory, xml_file)
            html_content = transform_xml_to_html(xml_path)

            # Create HTML file for each recipe
            recipe_name = os.path.splitext(xml_file)[0]
            output_file = os.path.join(output_directory, f'{recipe_name}.html')

            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(html_content)

            print(f'Generated: {output_file}')

# Main execution
if __name__ == '__main__':
    generate_recipe_pages()