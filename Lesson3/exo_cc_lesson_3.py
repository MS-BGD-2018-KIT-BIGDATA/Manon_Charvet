#Implanter des bureaux commerciaux en Franve
#distance en voiture villes a villes de splus grandes villes de france
# Lyon Paris
#

#liste des 100 villes
#matrice des distances
#renvoyer un fichier csv


import requests
from bs4 import BeautifulSoup
import re
import json
import numpy as np
import pandas as pd
import time


#HTML code
def getSoupFromURL(url, method='get', data={}):
  if method == 'get':
    res = requests.get(url) #pour recevoir le contenu de l'url?
  elif method == 'post':
    res = requests.post(url, data=data) #HTTP POST request: pour envoyer les data sur url?
  else:
    return None

  if res.status_code == 200: #HTTP status code: 200=OK, 404=not found,...
    soup = BeautifulSoup(res.text, 'html.parser') #r.text = contenu HTML
    return soup
  else:
    return None



def getBiggestCities(url):
  soup = getSoupFromURL(url)  # code HTML ~ en version texte
  res = soup.find_all("td")

  list_cities = []
  for i in range(5,41,4):
    list_cities.append(res[i].text.strip())

  return list_cities


#Given two city names in France, return the distance in miles
def getDistance(city_start,city_end):
    distance_url = 'https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&origins=' + city_start + ',FR&destinations=' + city_end
    res = requests.get(distance_url)
    assert res.status_code == 200
    distance_code = json.loads(res.text) #json exposes an API

    return distance_code['rows'][0]['elements'][0]['distance']['text']


def buildMatrixDistance(url):
    list_cities = getBiggestCities(url)

    list_distances = []
    for city_start in list_cities:
        for city_end in list_cities:
            list_distances.append(getDistance(city_start,city_end))

    matrix_distance = np.asarray(list_distances)
    matrix_distance = matrix_distance.reshape(len(list_cities),len(list_cities))

    df = pd.DataFrame(matrix_distance)
    df.columns = list_cities
    df['Villes'] = list_cities

    return df.set_index('Villes')


def main():
    url = 'https://lespoir.jimdo.com/2015/03/05/classement-des-plus-grandes-villes-de-france-source-insee/'

    start_time = time.time()


    print(buildMatrixDistance(url))

    end_time = time.time()
    print(round(end_time - start_time, 2), 'seconds')



if __name__ == '__main__':
      main()
