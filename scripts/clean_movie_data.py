# get a list of media types from making a set of of all the values in all the lists in that column
# get a list of production companies from making a set of all the values in all the lists in that column
# still have to clean year_end stuff (should be 2022 if blank). can i get this elsewhere? 

import pandas as pd
import re
import ast
import numpy as np
import os

def has_numbers(inputString):
     return any(char.isdigit() for char in inputString)
     
path = os.getcwd()
path = path.split('/')
path = '/'.join(path[:-1])     

dataframe = pd.read_csv(f"{path}/data/raw_snl_movies_data.csv") #still some issue in how it's processing data
mediums = dataframe['media_type'].to_list()
mediums.sort()
all_mediums = []
for index, row in dataframe.iterrows():
    list_of_info = dataframe['media_type'].values[row.name]
    print(list_of_info)
    try:
        list_of_info = ast.literal_eval(list_of_info)
        for elem in list_of_info:
            if has_numbers(elem) == False:
                all_mediums.append(elem)
    except ValueError:
        pass
    all_mediums = list(set(all_mediums))
    all_mediums.sort()
    med_txt = open(f'{path}/data/mediums.txt', 'w')
    for i in all_mediums:
        med_txt.write(str(i) + "\n")
    med_txt.close()

all_genres = []
for index, row in dataframe.iterrows():
    list_of_info = dataframe['genres'].values[row.name]
    print(list_of_info)
    try:
        list_of_info = ast.literal_eval(list_of_info)
        for elem in list_of_info:
            if has_numbers(elem) == False:
                all_genres.append(elem)
    except ValueError:
        pass
    all_genres = list(set(all_genres))
    gen_txt = open(f'{path}/data/genres.txt', 'w')
    for i in all_genres:
        gen_txt.write(str(i) + "\n")
    gen_txt.close()

production_companies = dataframe['production_companies'].to_list() #to_list?
#dataframe['media_type'] = dataframe['media_type'].astype(float)
all_production_companies = []
for index, row in dataframe.iterrows():
    prodcomp = dataframe['production_companies'].values[row.name]
    try:
        prodcomp = ast.literal_eval(prodcomp)
        for elem in prodcomp:
            all_production_companies.append(elem)
    except:
        pass
all_production_companies = list(set(all_production_companies)) #use this list to create a mediums list
prod_txt = open(f'{path}/data/production_companies.txt', 'w')
for i in all_production_companies:
    prod_txt.write(str(i) + "\n")
prod_txt.close()

####

mediums = ['TV Special','TV Movie','Video','TV Short','TV Series','TV Mini Series','Podcast Series','Video Game']

dataframe['medium'] = ''
dataframe['year_start'] = ''
dataframe['year_end'] = ''

for index, row in dataframe.iterrows():
    list_of_info = dataframe['media_type'].values[row.name]
    try:
        list_of_info = ast.literal_eval(list_of_info)
        revised_list = []
        crossover = [i for i in list_of_info if i in mediums]
        if len(crossover) > 0:
            dataframe.at[row.name,'medium'] = crossover
        else:
            dataframe.at[row.name, 'medium'] = ['Film']
        for item in list_of_info:
            item = item.strip()
            non_number = re.compile(r'[^\d]+')
            new_item = non_number.sub('',item)
            revised_list.append(new_item)
            years_list = []
            for item in revised_list:
                out = [(item[i:i+4]) for i in range(0, len(item), 4)]
            for year in out:
                if len(year) == 4 and int(year) > 1414:
                    years_list.append(year)
            if len(years_list) != 0:
                dataframe.at[row.name,'year_start'] = str(min(years_list))
                dataframe.at[row.name,'year_end'] = str(max(years_list))
    except ValueError:
        pass

dataframe.to_csv(f"{path}/data/cleaned_snl_movies_data.csv", index=False)
