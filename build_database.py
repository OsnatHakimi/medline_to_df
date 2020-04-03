import os
import pandas as pd
import glob
import pickle
from collections import defaultdict

def convert_medline(file):

    ''' Convert compacted Medline .txt file into single entries
        file: .txt file '''

    if not os.path.exists('./data'):
        os.makedirs('./data')

    with open(file) as data_file:
        block = ""
        found = False
        x = 0
        for line in data_file:
            if found:
                block += line
                if line.startswith("SO"):
                    x = x + 1
                    found = False
                    with open('./data/' + str(pmid) + ".txt", "w") as file:
                        file.write(block)
                        block = ""
            else:
                if line.startswith("PMID"):
                    found = True
                    block += line
                    pmid = line.split('-')[1].replace(' ','')

def parse_medline(file):

    ''' Parse a single Medline entry
        file: .txt file of a single Medline entry
        Output: dictionary '''

    def variate_entries(list):
        return ['{}- '.format(x) for x in list] + ['{} - '.format(x) for x in list] + ['{}  - '.format(x) for x in list]
        
    l = []
    with open(file) as f:
        content = f.readlines()
        copy = content.copy() + ['EOF']
        text=''
        loop=False
        for idx, line in enumerate(content):
            if copy[idx+1].startswith(tuple(variate_entries(medline_fields))) or copy[idx+1] == 'EOF':
                if loop:
                    text+=line
                    l.append(text)
                    text=''
                    loop=False
                else:
                    l.append(line)
            else:
                text+=line
                loop=True

    d = defaultdict(list)
    for line in list(set(l)):
        element = line.split('-')
        d[element[0].replace(' ','')].append('-'.join(element[1:]))

    for entry in d:
        d[entry] = ';'.join(d[entry])

    return d

if '__main__' == __name__:

    convert_medline('./pubmed_result_all_3_medline.txt')

    medline_fields = [line.rstrip('\n') for line in open('./medline_fields.txt')][0].split(',')
    medline_fields.sort()

    files = glob.glob('./data/*.txt')
    files = [parse_medline(file) for file in files]
    df = pd.DataFrame(files)
    pickle.dump(df, open("biomaterials.db", "wb"))
