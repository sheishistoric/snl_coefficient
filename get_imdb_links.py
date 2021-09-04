# preparing the data - get the imdb links for all the writers and performers on SNL.

import json
import ssl
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import pandas as pd
from urllib.parse import urlencode
import urllib

#######
performers = pd.read_csv("actors.csv")
performers['imdb_link'] = ''
writers = pd.read_csv("writers.csv")
writers['imdb_link'] = ''

def get_web_page_content(url):
  req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
  webpage = urlopen(req).read()
  soup = BeautifulSoup(webpage, 'html.parser')
  return soup

def get_href(person):
  person = person.split('(')[0]
  person = person.strip()
  edited_name = urllib.parse.quote_plus(person)
  search_url = 'https://www.imdb.com/find?q=' + edited_name + '&s=nm&exact=true&ref_=fn_nm_ex'
  soup = get_web_page_content(search_url)
  for a in soup.find_all('a', href=True):
    link = a.string
    if link == person:
      href = a['href']
      href = 'https://www.imdb.com' + href
      return href

def get_person_imdb(dataframe, row, column):
    z = row.name
    person = dataframe["person"].values[z]
    print(person)
    imdb_link = get_href(person)
    dataframe.at[z,column]= imdb_link

performers.apply(lambda row: get_person_imdb(performers, row, "imdb_link"), axis=1)
writers.apply(lambda row: get_person_imdb(writers, row, "imdb_link"), axis=1)

performers.to_csv('actors.csv', index=False)
writers.to_csv('writers.csv', index=False)