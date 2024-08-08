#!/usr/bin/python3
"""
This is a script to convert a Markdown file to HTML.

Usage:
    ./markdown2html.py [input_file] [output_file]

Arguments:
    input_file: the name of the Markdown file to be converted
    output_file: the name of the output HTML file

Example:
    ./markdown2html.py README.md README.html
"""

import sys
import os
import re
import hashlib

def markdown_to_html(markdown_content):
    html_lines = []
    in_list = False
    in_ordered_list = False
    current_paragraph = []

    def close_current_paragraph():
        if current_paragraph:
            # Join the lines of the current paragraph with line breaks
            paragraph_text = ' '.join(current_paragraph).replace('\n', '<br />')
            # Replace Markdown bold syntax with HTML tags
            paragraph_text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', paragraph_text)
            paragraph_text = re.sub(r'__(.*?)__', r'<em>\1</em>', paragraph_text)
            # Replace [[text]] with MD5 hash
            paragraph_text = re.sub(r'\[\[(.*?)\]\]', lambda m: hashlib.md5(m.group(1).encode()).hexdigest(), paragraph_text)
            # Remove all occurrences of 'c' (case insensitive) from ((text))
            paragraph_text = re.sub(r'\(\((.*?)\)\)', lambda m: m.group(1).replace('c', '').replace('C', ''), paragraph_text)
            html_lines.append(f'<p>{paragraph_text}</p>')
            current_paragraph.clear()

    for line in markdown_content:
        line = line.rstrip()
        
        # Handle headings
        if line.startswith('# '):
            close_current_paragraph()
            html_lines.append(f'<h1>{line[2:].strip()}</h1>')
        elif line.startswith('## '):
            close_current_paragraph()
            html_lines.append(f'<h2>{line[3:].strip()}</h2>')
        elif line.startswith('### '):
            close_current_paragraph()
            html_lines.append(f'<h3>{line[4:].strip()}</h3>')
        elif line.startswith('#### '):
            close_current_paragraph()
            html_lines.append(f'<h4>{line[5:].strip()}</h4>')
        elif line.startswith('##### '):
            close_current_paragraph()
            html_lines.append(f'<h5>{line[6:].strip()}</h5>')
        elif line.startswith('###### '):
            close_current_paragraph()
            html_lines.append(f'<h6>{line[7:].strip()}</h6>')
        
        # Handle unordered lists
        elif line.startswith('- '):
            close_current_paragraph()
            if not in_list:
                html_lines.append('<ul>')
                in_list = True
                in_ordered_list = False
            html_lines.append(f'<li>{line[2:].strip()}</li>')
        
        # Handle ordered lists
        elif line.startswith('* '):
            close_current_paragraph()
            if not in_ordered_list:
                html_lines.append('<ol>')
                in_ordered_list = True
                in_list = False
            html_lines.append(f'<li>{line[2:].strip()}</li>')
        
        # Handle blank lines or new paragraphs
        elif line == '':
            close_current_paragraph()
            if in_list:
                html_lines.append('</ul>')
                in_list = False
            if in_ordered_list:
                html_lines.append('</ol>')
                in_ordered_list = False
        
        else:
            # Add content to the current paragraph
            current_paragraph.append(line)
    
    # Close any open lists or paragraphs
    close_current_paragraph()
    if in_list:
        html_lines.append('</ul>')
    if in_ordered_list:
        html_lines.append('</ol>')
    
    return '\n'.join(html_lines)

def main():
    if len(sys.argv) != 3:
        print("Usage: ./markdown2html.py README.md README.html", file=sys.stderr)
        sys.exit(1)
    
    markdown_file = sys.argv[1]
    output_file = sys.argv[2]
    
    if not os.path.isfile(markdown_file):
        print(f"Missing {markdown_file}", file=sys.stderr)
        sys.exit(1)
    
    with open(markdown_file, 'r') as md_file:
        markdown_content = md_file.readlines()
    
    html_content = markdown_to_html(markdown_content)
    
    with open(output_file, 'w') as html_file:
        html_file.write(html_content)
    
    sys.exit(0)

if __name__ == "__main__":
    main()
