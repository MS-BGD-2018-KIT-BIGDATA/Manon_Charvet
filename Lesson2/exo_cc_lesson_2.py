#concurrent c discount fait plus de discount (ACER vs dell sur cdiscount): % de rebate, qu'est ce qui estle plus soldé
#ancien prix nouveau prix

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



def getDiscount(url):
    soup = getSoupFromURL(url)  # code HTML ~ en version texte

    class_avant = "prdtPrSt"
    class_apres = "prdtPrice"

    content_avant=soup.find_all(class_=class_avant)[0].text.strip()
    content_apres=soup.find_all(class_=class_apres)[0].text.strip()

    if '€' in content_apres: #pour enlever l'euro et ensuite pouvoir convertir en nombre
      parts = content_apres.split('€')
      content_apres =  int(parts[0]) + int(parts[1])*0.01
    else:
      content_apres = int(content_apres)


    if ',' in content_avant: #pour enlever la virgule et ensuite pouvoir convertir en nombre
      parts = content_avant.split(',')
      content_avant =  int(parts[0]) + int(parts[1])*0.01
    else:
      content_avant = int(content_avant)


    return round(((content_avant-content_apres)*100)/content_apres,2)



# Appelle des fonctions
def main():
    url = 'https://www.cdiscount.com/search/10/ordinateur+portable+acer.html#_his_'
    url2 = 'https://www.cdiscount.com/search/10/ordinateur+portable+dell.html#_his_'

    #For only one laptop per brand
    print(getDiscount(url),'% de remise pour Acer')
    print(getDiscount(url2),'% de remise pour Dell')




if __name__ == '__main__':
    main()

