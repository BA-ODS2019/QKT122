import requests
import pandas as pd
import numpy as np
from pandas.io.json import json_normalize

api_key = 'o7ejhb48ohglbckt'

api_search_url = 'https://api.trove.nla.gov.au/v2/result'

params = {
    'q': 'mahatma+gandhi',
    'zone': 'newspaper',
    'key': api_key,
    'n': '100',
    'encoding': 'json'
}
response = requests.get(api_search_url, params=params)

print(response)

json = response.json()
Gandhi = json_normalize(json['response']['zone'][0]['records']['article'])
Gandhi.head()
Gandhi.dtypes

to_drop = ['category',
          'edition',
          'pageSequence',
          'relevance.score',
          'relevance.value',
           'snippet',
          'troveUrl',
          'url']
Gandhi.drop(to_drop, inplace=True, axis=1)
Gandhi.head()

Gandhi['id'].is_unique
Gandhi.set_index('id', inplace=True)
Gandhi.head()

#Laver en kolonne med årstal alene
extr = Gandhi['date'].str.extract(r'^(\d{4})', expand=False)
Gandhi['year'] = pd.to_numeric(extr)
Gandhi.head()

#Laver en title kolonne 
title = Gandhi['title.value'].str.extract(r'^(.*?)\s\(', expand=False)
Gandhi['title'] = title
Gandhi.head()

city = Gandhi['title.value']

Gandhi['city'] = city

sydney = city.str.contains('Sydney')
brisbane = city.str.contains('Brisbane')
deniliquin = city.str.contains('Deniliquin')
toowoomba = city.str.contains('Toowoomba')
adelaide = city.str.contains('Adelaide')
cairns = city.str.contains('Cairns')
rockhampton = city.str.contains('Rockhampton')
perth = city.str.contains('Perth')

Gandhi['city'] = np.where(sydney, 'Sydney', np.where(rockhampton, 'Rockhampton', np.where(perth, 'Perth', np.where(deniliquin, 'Deniliquin', np.where(cairns, 'Carins', np.where(adelaide, 'Adelaide', np.where(brisbane, 'Brisbane', np.nan)))))))
Gandhi['city'].head(20)

to_drop = ['title.value',
          'title.id']
Gandhi.drop(to_drop, inplace=True, axis=1)
Gandhi.head()

print(Gandhi.head()) #viser de første 5 linier af filen for at få en forståelse af dataen
print(len(Gandhi)) #Antal rows
print(Gandhi.shape) #antal rows & columns 
print(Gandhi.size) #antal celler i hele filen
print(Gandhi.columns) #Navnene til columns
print(Gandhi.dtypes)