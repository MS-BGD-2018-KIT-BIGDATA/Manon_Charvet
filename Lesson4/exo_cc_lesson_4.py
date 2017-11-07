import requests
from bs4 import BeautifulSoup
import re
import json
import numpy as np
import pandas as pd
import time

#labo
#equivalent traitement (20 comprimés à 10mg = 10comprimés à 20mg)
#anne commercialisation
#mois commercialisation
#prix
#restriction age
#restriction poids



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



def getInfosFromCode(url):
    soup = getSoupFromURL(url)
    res_med = requests.get(url)
    #print(json.loads(res_med.text))

    # *********************
    # LABO:
    titulaires = json.loads(res_med.text)['titulaires']
    #print(titulaires[0])

    # *********************
    # EQUIVALENT TRAITEMENT
    denomination = json.loads(res_med.text)['denomination']
    regex_chiffres = re.compile('\d+')
    libelle = json.loads(res_med.text)['presentations'][0]['libelle']
    eq_trait = int(regex_chiffres.findall(denomination)[0]) * int(regex_chiffres.findall(libelle)[0])
    #print(eq_trait)

    # *********************
    # annee commercialisation & mois commercialisation:
    date = json.loads(res_med.text)['presentations'][0]['dateDeclarationCommercialisation']
    annee_com = date.split("-")[0]
    mois_com = date.split("-")[1]
    #print(annee_com)
    #print(mois_com)

    # *********************
    # prix
    prix = json.loads(res_med.text)['presentations'][0]['prix']
    #print(prix)

    # *********************
    # restriction: age & poids: indicationsTherapeutiques
    indications = json.loads(res_med.text)['indicationsTherapeutiques']
    #print(indications)
    regex_poids = re.compile('([\d.]+)\s+(lbs?|oz|g|kg) ')
    regex_age = re.compile('([\d.]+)\s+(ans?)')
    indic_poids = regex_poids.findall(indications)
    indic_age = regex_age.findall(indications)
    #print(indic_poids[0][0])
    #print(indic_age[0][0])

    return [titulaires[0], eq_trait, annee_com, mois_com, prix, indic_poids[0][0], indic_age[0][0]]



def main():



     url = 'https://open-medicaments.fr/api/v1/medicaments?query=ibuprofene'
     res = requests.get(url)
     assert res.status_code == 200

     med = json.loads(res.text)  # json exposes an API
     print(med)



     # Code Médicament
     code = med[1]['codeCIS'] #item 0 en ML
     #print(med[0])
     print('code: ',code)


     database = []
     for i in range(1,2):
         code = med[i]['codeCIS']
         url_med = 'https://open-medicaments.fr/api/v1/medicaments/' + code
         database.append(getInfosFromCode(url_med))



     database_matrix = np.asarray(database)

     columns = ["Laboratoire", "Equivalence_traitement", "annee_commercialisation", "mois_commercialisation","prix","indication_poids", "indication_age"]
     df = pd.DataFrame(database_matrix, columns=columns)

     df.to_csv("open-medicaments.csv")







if __name__ == '__main__':
        main()