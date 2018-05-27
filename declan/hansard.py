import sys
import os
import re
import random
from bs4 import BeautifulSoup
import csv
import pprint


hansard_loc = '../hansard2010to2018/'


nz_question_regex = '<p class="SubsQuestion">[^:]*?to the [\w <>\/]*<\/strong>: (?:.(?!<\/p>))*.<\/p><p class="SubsAnswer"><a name="time_\d{8}'
nz_q_bank_regex = '<p class="SubsQuestion">[^:]*?>([^>]*) \(([^\)]*)\)<\/strong> to the <strong>([\w <>\/]*)<\/strong>: ((?:.(?!<\/p>))*.)<\/p><p class="SubsAnswer"><a name="time_(\d{8})'
nz_parties = '(National|NZ First|Labour|Green|ACT|Leader of the Opposition|M\xc4\x81ori Party)'

uk_parties = set()

globalMemberDict = {
  "Edward Miliband" : ["Lab", "Doncaster North"],
  "Jeremy Corbyn" : ["Lab", "Islington North"],
  "Damian Green" : ["Con", "Ashford"],
  "Angus Robertson": ["SNP", "Moray"],
  "David Lidington" : ["Con", "Aylesbury"],
  "Harriet Harman" : ["Lab", "Camberwell and Peckham"],
  "George Osborne": ["Con", "Tatton"],
  "William Hague" : ["Con", "Richmond"],
  "Chris Grayling": ["Con", "Epsom and Ewell"],
  "Michael Connarty": ["Lab", "Linlithgow and East Falkirk"]
}

globalList = globalMemberDict.keys()


# def processfile(f):
#     questions = []
#     for line in f:
#         matches = re.findall(nz_question_regex, line)
#         questions.extend(matches)
#     print('Qs: ' + str(len(questions)))
#     q_bank = []
#     for q in questions:
#         matches = re.findall(nz_q_bank_regex, q)
#         build = []
#         for i in range(0, len(matches[0])):
#             build.append(re.sub('<strong>', '', re.sub(r'<\/strong>', '', matches[0][i])))
#         party = re.search(nz_parties, build[1])
#         if party:
#             build[1] = party.group(0)
#         else:
#             print(build)
#         q_bank.append(build)
#     print('QB: ' + str(len(q_bank)))
#     return q_bank

# def processfilenew(f):
#     file = f.read()
#     questions = []
#     matches = re.findall(nz_question_regex, file, re.MULTILINE)
#     questions.extend(matches)
#     print('Qs: ' + str(len(questions)))
#     n_bank = []
#     for q in questions:
#         matches = re.findall(nz_q_bank_regex, q)
#         build = []
#         for i in range(0, len(matches[0])):
#             build.append(re.sub('<strong>', '', re.sub(r'<\/strong>', '', matches[0][i])))
#         party = re.search(nz_parties, build[1])
#         if party:
#             build[1] = party.group(0)
#         # else:
#         #     print(build)
#         n_bank.append(build)
#     print('NB: ' + str(len(n_bank)))
#     return(n_bank)

def newProcess(f):
    questions = []
    localDict = {}
    localList = []
    hsoup = BeautifulSoup(f, 'html.parser')
    c = 0
    cg = 0
    co = 0
    questions = []
    # for q in hsoup.find_all('p', class_='Question'):
    parties = {}
    constituencies = {}
    names = {}
    save_num = 0
    save_id = 0
    for q in hsoup.find_all('li'):
        n = q.find('a', title="View member's contributions")
        if n is None:
            pass
        else:
            if 'Prime Minister' in n.text or 'Speaker' in n.text:
                pass
            else:
                # Extract the name, party and constituency
                name = ''
                constituency = ''
                party = ''
                q_num = 0
                q_id = 0
                # memCons = ''

                member = re.search(r'([^\(]*)\s+\(([\w\s\(\)\,-]+?)\)\s+?\(([^\)]*)\)', n.text)
                memSurnameRE = re.search(r'^(?:Mr|Mrs|Ms|Dr)[\. ]+(\w[\w ]+)', n.text)
                memMinisterRE = re.search(r'\((?:\w+ )+(\w+)\)$', n.text)
                memName = False
                if member:
                    memName = member.group(1)
                    memCons = member.group(2)
                    memPart = member.group(3)
                    localList.append(memName)
                    localDict[memName] = [memPart, memCons]
                elif memSurnameRE:
                    memSurname = memSurnameRE.group(1)
                    for item in localList:
                        if memSurname in item:
                            memName = item
                            memPart = localDict[memName][0]
                            memCons = localDict[memName][1]
                    if memName == False:
                        for item in globalList:
                            if memSurname in item:
                                memName = item
                                memPart = globalMemberDict[memName][0]
                                memCons = globalMemberDict[memName][1]
                elif n.text in localList:
                    memName = n.text
                    memPart = localDict[memName][0]
                    memCons = localDict[memName][1]
                    pass
                elif n.text in globalList:
                    memName = n.text
                    memPart = globalMemberDict[memName][0]
                    memCons = globalMemberDict[memName][1]
                elif memMinisterRE:
                    name = memMinisterRE.group(1)
                    for item in globalList:
                        if name in item:
                            memName = item
                            memPart = globalMemberDict[memName][0]
                            memCons = globalMemberDict[memName][1]
                else:
                    pass

                # Get the question asked
                question = ''
                for p in q('p'):
                    question += ' ' + p.text

                # Is it a follow-up?
                followup = False
                if len(q('p', class_="Question")) == 0:
                    followup = True
                    q_num = save_num
                    q_id = save_id
                else:
                    q_i = re.findall('Q?(\d\d?) ?\.\s*(.*)\[(\d*)\]', question)
                    q_num = q_i[0][0]
                    save_num = q_i[0][0]
                    question = q_i[0][1]
                    q_id = q_i[0][2]
                    save_id = q_i[0][2]

                # Get the URL
                url = ''
                for u in q('a', title="Share this contribution"):
                    url = u.get('data-hop-popover')

                # Print what we've got so far
                # print('NEW QUESTION')
                # print(name + ' - ' + constituency + ' - ' + party)
                # print(question)
                # print(url)
                # print('')

                date = int(os.path.basename(f.name).replace('-', '').replace('.html', ''))
                memAffi = findAffi(memPart, date)
                if memAffi == 'gov':
                    cg += 1
                else:
                    co += 1

                if memName is not False:
                    # print('Name ' + memName)
                    q_dict = {}
                    q_dict['Question'] = question
                    q_dict['memName'] = memName
                    q_dict['memCons'] = memCons
                    q_dict['memPart'] = memPart
                    q_dict['date'] = date
                    q_dict['memAffi'] = memAffi
                    q_dict['followup'] = followup
                    q_dict['qnum'] = q_num
                    q_dict['qid'] = q_id
                    c += 1
                    uk_parties.add(memPart)
                    questions.append(q_dict)
    return questions


brown1 = ['Lab', 'Lab/Co-op', 'Lab/ Co-op']
camclegg = ['Con', 'LD']
cam2 = ['Con']
may1 = ['Con']
may2 = ['Con']
may2cas = ['DUP']

def findAffi(party, date):
    gov = []
    cas = []
    # Determine the government
    if date <= 20100511:
        gov = brown1
    elif date <= 20150508:
        gov = camclegg
    elif date <= 20160713:
        gov = cam2
    elif date <= 20170611:
        gov = may1
    else:
        gov = may2
        cas = may2cas
    # Is this part in government?
    if party in gov:
        return 'gov'
    elif party in cas:
        return 'cas'
    else:
        return 'opp'


q_bank = []
print('QB Length: ' + str(len(q_bank)))
count = 0
countg = 0
counto = 0
for fname in os.listdir(hansard_loc):  # type: str
    print(fname)
    if fname[0] == '.':
        continue
    path = os.path.join(hansard_loc, fname)
    f = open(path, 'r', encoding='utf-8')
    q_bank.extend(newProcess(f))
    # print('Sample' + str(random.choice(q_bank)))

    # counts = newProcess(f)
    # count += counts[0]
    # countg += counts[1]
    # counto += counts[2]
    # print('g' + str(countg) + ' o' + str(counto))
    f.close()

print('QB Length: ' + str(len(q_bank)))


def d_dict_to_csv(dic):
    keys = dic[0].keys()
    print(keys)
    with open('../data/qbank.csv', 'w', newline='',encoding='utf-8') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(dic)
    return


d_dict_to_csv(q_bank)

print("And now...")





# f=open("q_bank.txt", "a+")
#
# wr = csv.writer(f, delimiter="^")
# wr.writerows(q_bank)
#
#
# f.close()


# for n in nn:
        #     if 'Prime Minister' in n.text or 'Speaker' in n.text:
        #         break
        # else :
        #     nn = q.find('a', title="View member's contributions")
        #     c += 1
        #     print(nn.text)
        # if len(nn) > 1:
        #     print('NOOOOOOO')
    # print(f.name + ': ' + str(c))


def hansard_reader(src_filename, class_func = None) :
    """ Based on an Iterator for the Penn-style distribution of the Stanford
        Sentiment Treebank. The iterator yields (question, affi) pairs.


        Parameters
        ----------
        src_filename : str
            Full path to the file to be read. CURRENTLY THE Q_DICT!
        class_func : None, or function mapping {'gov', 'opp', 'cas'} to
            another set of labels.


        Yields
        ------
        (question, affi)
            str, str in {'gov', 'opp', 'cas'}

        """
    if class_func is None:
        class_func = lambda x: x
    with open(src_filename, encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for q in reader:
            yield (q['Question'], q['memAffi'])

print(next(hansard_reader('../data/qbank.csv')))
print(next(next(hansard_reader('../data/qbank.csv'))))
print(next(next(next(hansard_reader('../data/qbank.csv')))))