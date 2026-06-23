#!/usr/bin/env python3
"""
Split long answers into numbered bullet points with circled numbers (①②③...).

Usage:
    Run from the unpacked docx directory (where word/document.xml exists).
    python split_answers.py

Each answer paragraph (red text with semicolons) is split into multiple paragraphs,
each starting with a circled number and on its own line.
"""
import re
import os

CIRCLED = ['①', '②', '③', '④', '⑤', '⑥', '⑦', '⑧', '⑨', '⑩',
           '⑪', '⑫', '⑬', '⑭', '⑮', '⑯', '⑰', '⑱', '⑲', '⑳']

def make_answer_para(text, para_id):
    """Create a new paragraph XML for an answer line."""
    return (
        f'    <w:p w14:paraId="{para_id}">\n'
        f'      <w:pPr>\n'
        f'        <w:numPr>\n'
        f'          <w:ilvl w:val="0"/>\n'
        f'          <w:numId w:val="0"/>\n'
        f'        </w:numPr>\n'
        f'        <w:ind w:leftChars="0"/>\n'
        f'        <w:rPr>\n'
        f'          <w:rFonts w:hint="eastAsia"/>\n'
        f'        </w:rPr>\n'
        f'      </w:pPr>\n'
        f'      <w:r>\n'
        f'        <w:rPr>\n'
        f'          <w:rFonts w:hint="eastAsia"/>\n'
        f'          <w:color w:val="FF0000"/>\n'
        f'        </w:rPr>\n'
        f'        <w:t xml:space="preserve">{text}</w:t>\n'
        f'      </w:r>\n'
        f'    </w:p>'
    )

def main():
    xml_path = 'word/document.xml'
    if not os.path.exists(xml_path):
        print(f"ERROR: {xml_path} not found. Run from unpacked docx directory.")
        return

    with open(xml_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find all paragraph blocks
    para_pattern = re.compile(r'(<w:p w14:paraId="[^"]*">.*?</w:p>)', re.DOTALL)
    paras = para_pattern.findall(content)

    new_paras = []
    pid_counter = 0
    split_count = 0

    for para in paras:
        # Check if this is a red answer paragraph with semicolons
        if '<w:color w:val="FF0000"/>' in para and '；' in para:
            # Extract the answer text
            text_match = re.search(r'<w:t[^>]*>(.*?)</w:t>', para)
            if text_match:
                answer_text = text_match.group(1)
                # Skip question lines (start with number + period)
                if re.match(r'^\d+\.', answer_text):
                    new_paras.append(para)
                    continue

                # Split by semicolons
                points = [p.strip() for p in answer_text.split('；') if p.strip()]

                if len(points) > 1:
                    for i, point in enumerate(points):
                        if i < len(CIRCLED):
                            numbered = f'{CIRCLED[i]}{point}'
                        else:
                            numbered = f'{i+1}.{point}'
                        pid_counter += 1
                        new_paras.append(make_answer_para(numbered, f'C{pid_counter:08X}'))
                    split_count += 1
                else:
                    new_paras.append(para)
            else:
                new_paras.append(para)
        else:
            new_paras.append(para)

    # Reconstruct the document
    body_start = content.find('<w:body>') + len('<w:body>')
    body_end = content.find('</w:body>')

    new_body = '\n'.join(new_paras)
    new_content = content[:body_start] + '\n' + new_body + '\n  ' + content[body_end:]

    with open(xml_path, 'w', encoding='utf-8') as f:
        f.write(new_content)

    print(f'Done! Split {split_count} answers into {pid_counter} bullet points.')

if __name__ == '__main__':
    main()
