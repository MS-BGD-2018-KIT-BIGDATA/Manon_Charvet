import requests
from bs4 import BeautifulSoup

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


#Chaque résultat de comptes
def getAccountsStatementsForPage(url, classname,content):
  soup = getSoupFromURL(url) #code HTML ~ en version texte
  if soup:

    #renvoie des chiffres avec un espace de type 2 308
    if ' ' in content: #pour enlever l'espace et ensuite pouvoir convertir en nombre
      parts = content.split(' ')
      return int(parts[0])*1000 + int(parts[1])
    else:
      return int(content)
  else:
    0

def getABCDPerYearPerInhabitants(url,classname):
    soup = getSoupFromURL(url)  # code HTML ~ en version texte
    A_content=soup.find_all(class_=classname)[1].text.strip()
    B_content=soup.find_all(class_=classname)[4].text.strip()
    C_content=soup.find_all(class_=classname)[10].text.strip()
    D_content=soup.find_all(class_=classname)[13].text.strip()
    return [getAccountsStatementsForPage(url,classname,A_content),getAccountsStatementsForPage(url,classname,B_content),getAccountsStatementsForPage(url,classname,C_content),getAccountsStatementsForPage(url,classname,D_content)]


def getABCDPerYearPerStrate(url,classname):
    soup = getSoupFromURL(url)  # code HTML ~ en version texte
    A_content=soup.find_all(class_=classname)[2].text.strip()
    B_content=soup.find_all(class_=classname)[5].text.strip()
    C_content=soup.find_all(class_=classname)[11].text.strip()
    D_content=soup.find_all(class_=classname)[14].text.strip()
    return [getAccountsStatementsForPage(url,classname,A_content),getAccountsStatementsForPage(url,classname,B_content),getAccountsStatementsForPage(url,classname,C_content),getAccountsStatementsForPage(url,classname,D_content)]




# Appelle des fonctions
def main():
    url = 'http://alize2.finances.gouv.fr/communes/eneuro/detail.php?icom=056&dep=075&type=BPS&param=5&exercice='
    A_parhab_class = "montantpetit G"

    for i in range(2010,2016):
      print('-----')
      print('Pour l''année ' + str(i) + ', résultats par habitants de respectivement A, B, C et D: ')
      print(getABCDPerYearPerInhabitants(url + str(i), A_parhab_class))
      print('Pour l''année ' + str(i) + ', résultats par strate de respectivement A, B, C et D: ')
      print(getABCDPerYearPerStrate(url + str(i), A_parhab_class))


if __name__ == '__main__':
    main()
