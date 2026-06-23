#!/usr/bin/env python3
"""
Add red-colored answers to a docx outline XML.

Usage:
    1. Place answers.json in the current directory (unpacked docx folder)
    2. Run: python add_answers.py
    3. answers.json format: {"question_text": "answer_text", ...}

The script finds each question in word/document.xml and inserts a red answer run.
"""
import json
import re
import sys
import os

def main():
    json_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'answers.json')
    if not os.path.exists(json_path):
        json_path = 'answers.json'

    if not os.path.exists(json_path):
        print(f"ERROR: answers.json not found at {json_path}")
        print("Place answers.json in the unpacked docx directory or alongside this script.")
        sys.exit(1)

    with open(json_path, 'r', encoding='utf-8') as f:
        answers = json.load(f)

    xml_path = 'word/document.xml'
    if not os.path.exists(xml_path):
        print(f"ERROR: {xml_path} not found. Run from unpacked docx directory.")
        sys.exit(1)

    with open(xml_path, 'r', encoding='utf-8') as f:
        content = f.read()

    success = 0
    fail = 0

    for question, answer in answers.items():
        escaped_q = re.escape(question)
        pattern = r'(<w:t>' + escaped_q + r'</w:t>)'
        match = re.search(pattern, content)
        if not match:
            print(f"WARNING: not found: {question}")
            fail += 1
            continue

        pos = match.end()
        end_p = content.find('</w:p>', pos)
        if end_p == -1:
            print(f"WARNING: no </w:p> for: {question}")
            fail += 1
            continue

        # Escape < and > in answer text
        safe_answer = answer.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

        answer_run = (
            '<w:r>'
            '<w:rPr>'
            '<w:rFonts w:hint="eastAsia"/>'
            '<w:color w:val="FF0000"/>'
            '</w:rPr>'
            '<w:t xml:space="preserve"> ' + safe_answer + '</w:t>'
            '</w:r>'
        )

        content = content[:end_p] + answer_run + content[end_p:]
        success += 1
        print(f"OK: {question}")

    with open(xml_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"\nDone! {success} added, {fail} failed.")

if __name__ == '__main__':
    main()
