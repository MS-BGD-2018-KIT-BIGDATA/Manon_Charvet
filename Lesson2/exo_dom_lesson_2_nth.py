import requests
from bs4 import BeautifulSoup
import re

#HTML de la page
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

##Méthode sans nth-of-type
##Chaque résultat de comptes
#def getAccountsStatementsForPage(url,content):
#  soup = getSoupFromURL(url) #code HTML ~ en version texte
#  if soup:
#
#    #renvoie des chiffres avec un espace de type 2 308
#    if ' ' in content: #pour enlever l'espace et ensuite pouvoir convertir en nombre
#      parts = content.split(' ')
#      return int(parts[0])*1000 + int(parts[1])
#    else:
#      return int(content)
#  else:
#    0

def getABCDPerYearPerInhabitants(url):
    soup = getSoupFromURL(url)  # code HTML ~ en version texte
    class_results = "libellepetit G"  # look for A, B, C and D
    res = soup.find_all("td", class_=class_results) #liste des colonnes (en gras) ou on peut identifier A,B,C,D

    #Ancienne methode sans utiliser nth-of-type
    #res = requests.get(url)
    #A_content=soup.find_all(class_=classname)[1].text.strip()
    #B_content=soup.find_all(class_=classname)[4].text.strip()
    #C_content=soup.find_all(class_=classname)[10].text.strip()
    #D_content=soup.find_all(class_=classname)[13].text.strip()

    content=[0,0,0,0]
    i=0
    for element in res:
        if re.search('= [ABCD]\Z', element.text): #recherche des lettres A,B,C,D
            subcontent=element.parent.select_one("td:nth-of-type(2)").text.strip() #permet de se promener dans la ligne
                                                                                   # associée a la lettre
            # renvoie des chiffres avec un espace de type 2 308
            if ' ' in subcontent:  # pour enlever l'espace et ensuite pouvoir convertir en nombre
                parts = subcontent.split(' ')
                subcontent = int(parts[0]) * 1000 + int(parts[1])
            else:
                subcontent = int(subcontent)
            content[i]=subcontent
            i=i+1

    return content


def getABCDPerYearPerStrate(url):
    soup = getSoupFromURL(url)  # code HTML ~ en version texte
    class_results = "libellepetit G"  # look for A, B, C and D
    res = soup.find_all("td", class_=class_results)

    # Version sans utiliser nth-of-type
    #A_content=soup.find_all(class_=classname)[2].text.strip()
    #B_content=soup.find_all(class_=classname)[5].text.strip()
    #C_content=soup.find_all(class_=classname)[11].text.strip()
    #D_content=soup.find_all(class_=classname)[14].text.strip()


    content=[0,0,0,0]
    i=0
    for element in res:
        if re.search('= [ABCD]\Z', element.text):
            subcontent=element.parent.select_one("td:nth-of-type(3)").text.strip()
            # renvoie des chiffres avec un espace de type 2 308
            if ' ' in subcontent:  # pour enlever l'espace et ensuite pouvoir convertir en nombre
                parts = subcontent.split(' ')
                subcontent = int(parts[0]) * 1000 + int(parts[1])
            else:
                subcontent = int(subcontent)
            content[i]=subcontent
            i=i+1

    return content

    #return [getAccountsStatementsForPage(url,classname,A_content),getAccountsStatementsForPage(url,classname,B_content),
            #getAccountsStatementsForPage(url,classname,C_content),getAccountsStatementsForPage(url,classname,D_content)]




# Appelle des fonctions
def main():
    url = 'http://alize2.finances.gouv.fr/communes/eneuro/detail.php?icom=056&dep=075&type=BPS&param=5&exercice='

    #results_class = "montantpetit G"
    #letter_column="libellepetit G" #to find the lines corresponding to A,B,C and D

    for i in range(2010,2016):
      print('-----')
      print('Pour l''année ' + str(i) + ', résultats par habitants de respectivement A, B, C et D: ')
      #print(getABCDPerYearPerInhabitants(url + str(i), results_class)) #Méthode sans nth-of-type
      print(getABCDPerYearPerInhabitants(url + str(i)))
      print('Pour l''année ' + str(i) + ', résultats par strate de respectivement A, B, C et D: ')
      #print(getABCDPerYearPerStrate(url + str(i), results_class)) #Méthode sans nth-of-type
      print(getABCDPerYearPerStrate(url + str(i)))






if __name__ == '__main__':
    main()
