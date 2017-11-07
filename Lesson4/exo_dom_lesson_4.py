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


def get_id_ad(url):
    soup = getSoupFromURL(url)  # code HTML ~ en version texte

    classname = "saveAd"
    res = soup.find_all(class_=classname)

    id_ad = []
    for element in res:
        id_ad.append(element['data-savead-id'])

    return id_ad


def get_infos_from_id_ad(ad_number,region):
    #ad_number = get_id_ad(url)


    url_car = 'https://www.leboncoin.fr/voitures/' + ad_number + '.htm?ca=12_s'

    # téléphone du propriétaire, est ce que la voiture est vendue par un professionnel ou un particulier
    #class_year = "property"


    #Version
    class_title = "no-border"
    soup = getSoupFromURL(url_car)
    res_title = soup.find_all(class_=class_title)
    #print(res_title[0].text)

    if re.findall(r"(?<=\bZOE\s)(\w+)", res_title[0].text.strip().upper()) or re.findall(r"(?<=\bZOÉ\s)(\w+)", res_title[0].text.strip().upper()):
        if 'ZOE' in res_title[0].text.strip().upper():
            #print(res_title[0].text.strip().upper())
            version = re.findall(r"(?<=\bZOE\s)(\w+)", res_title[0].text.strip().upper())[0]
        elif 'ZOÉ' in res_title[0].text.strip().upper():
            #print(res_title[0].text.strip().upper())
            version = re.findall(r"(?<=\bZOÉ\s)(\w+)", res_title[0].text.strip().upper())[0]
    #print(version)
    else:
        version = 'NaN'




    #Price, year, km
    class_year = "value"
    res = soup.find_all(class_=class_year)

    if '€' in res[0].text.strip():   ###price = res[0].text.strip().replace('€','')
        parts = re.findall("\d{1,4}", res[0].text)
        price = int(parts[0])*1000 + int(parts[1])

    if 'KM' in res[5].text.strip():
        parts_km = re.findall("\d{1,6}", res[5].text)
        #print(parts_km)
        if len(parts_km)>=2:
            km = int(parts_km[0])*1000 + int(parts_km[1])
        else:
            km = int(parts_km[0])

    year = res[4].text.strip()

    #????????????????????
    #Owner's phone number
    #class_phone = "button-orange large phoneNumber trackable"
    #class_phone = "phone_number font-size-up"
    #class_phone = "container"

    #res_phone = soup.find_all(class_=class_phone)
    #res_phone = soup.find_all("button")
    #res_phone = soup.find_all("href")

    #test = re.findall("\d{1,10}", res_phone)

    #print(res_phone)

    #print(test)
    #????????????????????

    #Pro or personnal owner
    #url_ispro = 'https://www.leboncoin.fr/voitures/offres/' + region + '/?q=renault%20zo%E9&brd=Renault&mdl=Zoe'
    #class_ispro = "ispro"
    #class_ispro = "line line_pro noborder"
    #class_ispro = "properties lineNegative"
    #res_ispro = soup.find_all(class_=class_ispro)
    #print(res_ispro[0].text.strip())

    #is_pro = re.findall(r"/\b($Pro)\b/i", res_ispro[0].text)
    #if re.search(r'\bPro\b', res_ispro[0].text):
    #    is_pro = True
    #else:
    #    is_pro = False


    #print(is_pro)



    #CALCUL DE L'ARGUS: sans tenir compte des km
    if version in {"INTENS","ZEN","LIFE"}:
        url_argus = "http://www.lacentrale.fr/cote-auto-renault-zoe-" + version + "+charge+rapide-" + year + ".html"

        soup = getSoupFromURL(url_argus)
        tmp_prix = soup.find_all("span", class_="jsRefinedQuot")[0].text.replace(" ", "")


        #print("argus",tmp_prix)
        argus = tmp_prix
    else:
        argus = "NaN"


    return [version, price, year, km, region, argus]
    #return [price, year, km]



def loopForOneRegion():

    regions = ['ile_de_france', 'provence_alpes_cote_d_azur','aquitaine']
    #regions = ['ile_de_france']

    database = []
    for region in regions:
        url = 'https://www.leboncoin.fr/voitures/offres/' + region + '/?q=renault%20zo%E9&brd=Renault&mdl=Zoe'



        list_ad = get_id_ad(url)
        #list_ad = list_ad
        for ad_nb in list_ad:
            #print(list_ad)
            database.append(get_infos_from_id_ad(ad_nb,region))

    database_matrix = np.asarray(database)

    return database_matrix


def compareArgus(database_matrix):

    columns = ["version", "price", "year", "km", "region", "Prix_Argus"]
    df = pd.DataFrame(database_matrix, columns=columns)




    #url_argus = "http://www.lacentrale.fr/cote-auto-renault-zoe-{}+charge+rapide{}-{}.html"

    #soup = getSoupFromURL(url_argus)
    #tmp_prix = soup.find_all("span", class_="jsRefinedQuot")[0].text.replace(" ", "")

    df.to_csv("compare_car.csv")

    return df



def main():


    start_time = time.time()

    #print(get_id_ad(url))
    #print(get_infos_from_id_ad(url))
    print(compareArgus(loopForOneRegion()))

    end_time = time.time()
    print(round(end_time - start_time, 2), 'seconds')



if __name__ == '__main__':
      main()
