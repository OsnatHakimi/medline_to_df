import re
import os
import pandas as pd


refs = "/home/osnat/Desktop/new_random_text/random_medline"
folder = "/home/osnat/Desktop/new_random_text"
prefix = "/random"


def convert_medline(refs):
    with open (refs) as data_file:
        block = ""
        found = False
        x = 0
        for line in data_file:
            if found:
                block += line
                if line.startswith("SO"):
                    x = x + 1
                    found = False
                    with open(folder + prefix + str(x) + ".txt", "w") as file:
                        file.write(block)
                        block = ""
            else:
                if line.startswith("PMID"):
                    found = True
                    block += line


all = []


def extract_gender_abstract(folder):
    abstracts = [os.path.join(folder, f) for f in os.listdir(folder)]
    for abstract in abstracts:
        dict = {'abstract':abstract[-15:-3],'PMID': 1234, 'Year': 1234, 'Humans':0, 'Animals':0, 'Female': 0, 'Male':0}
        with open(abstract) as f:
            content = f.readlines()
            for line in content:
                if line.startswith('PMID'):
                    dict['PMID'] = line[5:]
                elif line.startswith('MH  - Male'):
                    dict['Male'] = 1
                elif line.startswith('MH  - Female'):
                    dict['Female'] = 1
                elif line.startswith('MH  - Animals'):
                    dict['Animals'] = 1
                elif line.startswith('MH  - Humans'):
                    dict['Humans'] = 1
                elif line.startswith('DP'):
                    dict['Year'] = line[6:10]
        all.append(dict.copy())
        df = pd.DataFrame(all)
    print(df)
    df.to_csv('gender_year_background.csv', encoding='utf-8', index=False)








convert_medline('/home/osnat/Desktop/new_random_text/random_medline')
#extract_gender_abstract()










