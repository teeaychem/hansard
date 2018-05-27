import csv
import re


with open('../data/qbank.csv', encoding='utf-8') as f:
  reader = list(csv.DictReader(f))
  # print(reader)
  for q in reader:
    q['Question'] = re.sub(r'Prime(\s+Minister){0,1}', r'$person', q['Question'])
    q['Question'] = re.sub(r'(right\s+){0,1}hon\.(\s+(?:Friend|Member|Gentleman|Lady)){0,1}', r'$person', q['Question'])
    q['Question'] = re.sub(r'(right\s+){0,1}[Hh]on\.\s+(?:(?:Opposition\s+){0,1}Members)', r'$people', q['Question'])
    q['Question'] = re.sub(r'\s(?:[Hh]e|[Ss]he|[Hh]is|[Hh]er)\s', r' $pronoun ', q['Question'])
    # print(q)

keys = reader[0].keys()
with open('../data/qbankAnon.csv', 'w', newline='',encoding='utf-8') as output_file:
    dict_writer = csv.DictWriter(output_file, keys)
    dict_writer.writeheader()
    dict_writer.writerows(reader)

  # with open("../data/qbankAnon.csv", "w") as g:
  #     writer = csv.writer(g)
  #     writer.writerows(reader)