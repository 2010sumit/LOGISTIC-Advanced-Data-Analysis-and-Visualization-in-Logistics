"""
Convert Markdown Report into MS Word / Browser Compatible HTML
Author: SUMIT KUMAR (SUMIT277203YT@GMAIL.COM | 9120329201)
"""

import os
import re

def convert_md_to_html(md_path, html_path):
    with open(md_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Simple Markdown parser for Word compatibility
    html_out = f"""<!DOCTYPE html>
<html xmlns:o='urn:schemas-microsoft-com:office:office' xmlns:w='urn:schemas-microsoft-com:office:word' xmlns='http://www.w3.org/TR/REC-html40'>
<head>
<meta charset="utf-8">
<title>Logistics Simulation Analysis Report - SUMIT KUMAR</title>
<style>
    body {{
        font-family: Arial, sans-serif;
        line-height: 1.6;
        color: #333333;
        margin: 40px;
    }}
    h1 {{
        color: #1a365d;
        border-bottom: 2px solid #2b6cb0;
        padding-bottom: 8px;
    }}
    h2 {{
        color: #2c5282;
        margin-top: 30px;
        border-left: 4px solid #3182ce;
        padding-left: 10px;
    }}
    h3 {{
        color: #2b6cb0;
    }}
    table {{
        border-collapse: collapse;
        width: 100%;
        margin: 20px 0;
    }}
    th, td {{
        border: 1px solid #cbd5e0;
        padding: 10px;
        text-align: left;
    }}
    th {{
        background-color: #2d3748;
        color: #ffffff;
    }}
    tr:nth-child(even) {{
        background-color: #f7fafc;
    }}
    .profile-box {{
        background-color: #ebf8ff;
        border: 1px solid #bee3f8;
        padding: 15px;
        border-radius: 8px;
        margin-bottom: 20px;
    }}
    img {{
        max-width: 100%;
        height: auto;
        border: 1px solid #e2e8f0;
        margin: 15px 0;
    }}
    .recommendation-box {{
        background: #f0fff4;
        border-left: 5px solid #38a169;
        padding: 12px;
        margin-bottom: 15px;
    }}
</style>
</head>
<body>
"""
    # Replace markdown image syntax with HTML img tags
    content_html = re.sub(r'!\[(.*?)\]\((.*?)\)', r'<div style="text-align:center;"><img src="\2" alt="\1"><p><em>\1</em></p></div>', content)
    
    # Process basic markdown headers & formatting
    lines = content_html.split('\n')
    in_table = False
    table_html = []
    
    for line in lines:
        line_str = line.strip()
        if line_str.startswith('|') and line_str.endswith('|'):
            if not in_table:
                in_table = True
                table_html.append('<table>')
            cells = [c.strip() for c in line_str.split('|')[1:-1]]
            if '---' in cells[0]:
                continue
            is_header = len(table_html) == 1
            tag = 'th' if is_header else 'td'
            row_str = '<tr>' + ''.join([f'<{tag}>{c}</{tag}>' for c in cells]) + '</tr>'
            # Bold check inside cells
            row_str = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', row_str)
            table_html.append(row_str)
        else:
            if in_table:
                in_table = False
                table_html.append('</table>')
                html_out += '\n'.join(table_html)
                table_html = []
            
            if line_str.startswith('# '):
                html_out += f"<h1>{line_str[2:]}</h1>"
            elif line_str.startswith('## '):
                html_out += f"2.2 {line_str[3:]}" if "Pearson" in line_str else f"<h2>{line_str[3:]}</h2>"
            elif line_str.startswith('### '):
                html_out += f"<h3>{line_str[4:]}</h3>"
            elif line_str.startswith('- '):
                html_out += f"<li>{re.sub(r'\\*\\*(.*?)\\*\\*', r'<strong>\\1</strong>', line_str[2:])}</li>"
            elif line_str == '---':
                html_out += "<hr>"
            elif line_str:
                formatted_p = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', line_str)
                html_out += f"<p>{formatted_p}</p>"
                
    if in_table:
        table_html.append('</table>')
        html_out += '\n'.join(table_html)

    html_out += "</body></html>"

    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html_out)
        
    print(f"[+] Converted '{md_path}' to MS Word/Browser compatible '{html_path}'")

if __name__ == "__main__":
    convert_md_to_html("logistics_analysis_report.md", "logistics_analysis_report.html")
