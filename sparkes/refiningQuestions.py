import csv
import re


with open('../data/combinedQBank.csv', encoding='utf-8') as f:
  reader = list(csv.DictReader(f))
  # print(reader)
  for q in reader:
    q['Question'] = re.sub(r'[Pp]rime(\s+[Mm]inister){0,1}', r'$person', q['Question'])
    q['Question'] = re.sub(r'(right\s+){0,1}hon\.(\s+(?:[Ff]riend|[Mm]ember|[Gg]entleman|[Ll]ady)){0,1}', r'$person', q['Question'])
    q['Question'] = re.sub(r'(right\s+){0,1}[Hh]on\.\s+(?:(?:[Oo]pposition\s+){0,1}[Mm]embers)', r'$people', q['Question'])
    q['Question'] = re.sub(r'\s(?:[Hh]e|[Ss]he|[Hh]is|[Hh]er)\s', r' $pronoun ', q['Question'])
    q['Question'] = re.sub(r'\.([A-Z])', r'. \1', q['Question']) # spacing between sentences
    q['Question'] = re.sub(r'[A-Z]\w+(?: [A-Z]\w+)+', r'$person', q['Question']) # more people
    # print(q)

keys = reader[0].keys()

with open('../data/combinedQBankAnon2.csv', 'w', newline='',encoding='utf-8') as output_file:
    dict_writer = csv.DictWriter(output_file, keys)
    dict_writer.writeheader()
    dict_writer.writerows(reader)