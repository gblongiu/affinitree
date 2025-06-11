"""Utility script to generate questions.json from fullQuestionnare.txt."""
import json
import re

qs = []
with open('fullQuestionnare.txt') as f:
    lines = [line.strip() for line in f]

i = 0
while i < len(lines):
    line = lines[i]
    if re.match(r'^\d+\s', line):
        parts = line.split(None, 1)
        num = int(parts[0])
        question = parts[1] if len(parts) > 1 else ''
        if num != 241:
            qs.append({'id': num, 'text': question})
        i += 1
        while i < len(lines) and lines[i].strip() != '':
            i += 1
    else:
        i += 1

with open('questions.json', 'w') as f:
    json.dump({'questions': qs}, f, indent=2)
print('Wrote', len(qs), 'questions to questions.json')
