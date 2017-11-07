#1) Get the list of the 256 top contributors in Github
#2) Compute the average number of stars for each contributor
#3) Sort the contributors by the average number of stars

import requests
from bs4 import BeautifulSoup
import re
import json
import numpy as np
import pandas as pd
import time

#to get the token: https://github.com/settings/tokens
my_token = "fa81b2d14323b1fa1e7e37989bb38a74012794b2"

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


#Return contributors' name
def getTopContributors(url):
  soup = getSoupFromURL(url)  # code HTML ~ en version texte

  res = soup.find_all("th")

  user = []
  for element in res:
    if re.search("#\d{1,3}", element.text):
      user.append(element.parent.select_one("td:nth-of-type(1)").text)

  return user

#WITHOUT OAUTH / TOKEN
#Using GitHub API
#Return the average number of repositories stars for each user
def getAverageStarsNumber(user):
    pseudo = user.split(' ')[0]

    #Version 1 url
    #my_headers = {'Authorization': 'token {}'.format(my_token)}
    #user_url = 'https://api.github.com/users/' + pseudo + '/repos'
    #res = requests.get(user_url, headers = my_headers) # headers for authorization

    #Version 2 url
    user_url = 'https://api.github.com/users/' + pseudo + '/repos?access_token=fa81b2d14323b1fa1e7e37989bb38a74012794b2'

    res = requests.get(user_url)
    assert res.status_code == 200

    user_repositories = json.loads(res.text) #json exposes an API

    nb_of_stars = []
    for repo in user_repositories:
        nb_of_stars.append(repo['stargazers_count'])

    if nb_of_stars == []:
        avg_nb_stars = 0
    else:
        avg_nb_stars = np.mean(nb_of_stars)

    return round(avg_nb_stars,1)


def sumUpAndSort(url):
    users_list = getTopContributors(url)[:2]

    list_stars = []
    for user in users_list:
    #    print(user)
        list_stars.append(getAverageStarsNumber(user))


    return pd.Series(index=users_list, data=list_stars).sort_values(ascending=False)


def main():
  url = 'https://gist.github.com/paulmillr/2657075' #List of top contributors

  start_time = time.time()
  print(sumUpAndSort(url))
  end_time = time.time()
  print(round(end_time-start_time,2), 'seconds')



if __name__ == '__main__':
      main()
