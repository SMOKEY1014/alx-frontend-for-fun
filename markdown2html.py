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
    extr_prg = []

    def close_extr_prg():
        r = r'\[\[(.*?)\]\]'

        if extr_prg:
            prg_txt = ' '.join(extr_prg).replace('\n', '<br />')
            prg_txt = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', prg_txt)
            prg_txt = re.sub(r'__(.*?)__', r'<em>\1</em>', prg_txt)
            prg_txt = re.sub(r, lambda m: hashlib.md5(
                    m.group(1).encode()).hexdigest(), prg_txt)

            prg_txt = re.sub(r, lambda m: m.group(1).replace(
                    'c', '').replace('C', ''), prg_txt)
            html_lines.append(f'<p>{prg_txt}</p>')

            extr_prg.clear()

    for line in markdown_content:
        line = line.rstrip()

        # Handle headings
        if line.startswith('# '):
            close_extr_prg()
            html_lines.append(f'<h1>{line[2:].strip()}</h1>')
        elif line.startswith('## '):
            close_extr_prg()
            html_lines.append(f'<h2>{line[3:].strip()}</h2>')
        elif line.startswith('### '):
            close_extr_prg()
            html_lines.append(f'<h3>{line[4:].strip()}</h3>')
        elif line.startswith('#### '):
            close_extr_prg()
            html_lines.append(f'<h4>{line[5:].strip()}</h4>')
        elif line.startswith('##### '):
            close_extr_prg()
            html_lines.append(f'<h5>{line[6:].strip()}</h5>')
        elif line.startswith('###### '):
            close_extr_prg()
            html_lines.append(f'<h6>{line[7:].strip()}</h6>')

        # Handle unordered lists
        elif line.startswith('- '):
            close_extr_prg()
            if not in_list:
                html_lines.append('<ul>')
                in_list = True
                in_ordered_list = False
            html_lines.append(f'<li>{line[2:].strip()}</li>')

        # Handle ordered lists
        elif line.startswith('* '):
            close_extr_prg()
            if not in_ordered_list:
                html_lines.append('<ol>')
                in_ordered_list = True
                in_list = False
            html_lines.append(f'<li>{line[2:].strip()}</li>')

        # Handle blank lines or new paragraphs
        elif line == '':
            close_extr_prg()
            if in_list:
                html_lines.append('</ul>')
                in_list = False
            if in_ordered_list:
                html_lines.append('</ol>')
                in_ordered_list = False

        else:
            # Add content to the current paragraph
            extr_prg.append(line)

    # Close any open lists or paragraphs
    close_extr_prg()
    if in_list:
        html_lines.append('</ul>')
    if in_ordered_list:
        html_lines.append('</ol>')

    return '\n'.join(html_lines)


def main():
    if len(sys.argv) != 3:
        cmd = "./markdown2html.py"
        print("Usage: "+cmd+" README.md README.html", file=sys.stderr)
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
