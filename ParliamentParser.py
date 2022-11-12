from bs4 import BeautifulSoup
import requests
import json
import time
import random

headers = {
     'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36'
 }
# GetAllLinksAndNamesFromPolitics
res = requests.get(f'https://www.bundestag.de/ajax/filterlist/de/abgeordnete/biografien/862712-862712?limit=20&noFilterSet=true&offset=0',headers=headers)
with open('AllData.html','a',encoding='utf-8') as f:
    f.write(res.text)
i = 12
while(i <= 732):
   res2 = requests.get(f'https://www.bundestag.de/ajax/filterlist/de/abgeordnete/biografien/862712-862712?limit=20&noFilterSet=true&offset={i}', headers=headers)
   with open('AllData.html','a',encoding='utf-8') as f:
        f.write(res2.text)
   del res2
   print(i)
   time.sleep(5)
   i+=20

# FormJsonFromHTML
with open('AllData.html','r',encoding='utf-8') as f:
    fileRaw = f.read()
soup = BeautifulSoup(fileRaw,'html.parser')
names = soup.find_all('div',class_ = 'bt-bild-info-text')
politicNameForHref = []
politicHref = []

for name in names:
    politicNameForHref.append(name.find('p').text.strip())
PoliticLinkJson = {}
namesHref = soup.find_all('a',href=True)
for href in namesHref:
    politicHref.append(href['href'])
a = 0
while(a < len(namesHref)):
    PoliticLinkJson[politicNameForHref[a]] =  'https://www.bundestag.de' + politicHref[a]
    a+=1


with open('PoliticLinkJson.json','w',encoding='utf-8') as f:
    json.dump(PoliticLinkJson,f,indent=4,ensure_ascii=False)

# PoliticsData

socialNetworks ={}
Person ={}
Persons = []
Name = []
Occupation = []
count = 0

while(count<len(politicHref)):
        res3 = requests.get('https://www.bundestag.de'+politicHref[count] , headers=headers)
        soup2 = BeautifulSoup(res3.text,'html.parser')
        Facebook = soup2.find('a', {'title' : 'Facebook'})

        socialNetworks['Facebook'] = '' if Facebook is None else Facebook['href']

        Homepage = soup2.find('a', {'title' : 'Homepage'})

        socialNetworks['Homepage'] = '' if Homepage is None else Homepage['href']

        Youtube = soup2.find('a', {'title' : 'Youtube'})

        socialNetworks['Youtube'] = '' if Youtube is None else Youtube['href']

        Twitter= soup2.find('a', {'title' : 'Twitter'})

        socialNetworks['Twitter'] = '' if Twitter is None else Twitter['href']

        Instagram = soup2.find('a', {'title' : 'Instagram'})

        socialNetworks['Instagram'] = '' if Instagram is None else Instagram['href']

        LinkedIn= soup2.find('a', {'title' : 'Instagram'})

        socialNetworks['LinkedIn'] =  '' if LinkedIn is None else LinkedIn['href']

        Name = soup2.find('div' , 'bt-biografie-name').find('h3')

        Occupation = soup2.find('div',class_= 'bt-biografie-beruf')

        Person['name'] = '' if Name is None else Name.text.strip()
        Person['socialNetworks'] = socialNetworks.copy()
        Person['Occupation'] = '' if Occupation is None else Occupation.text.strip()
        Persons.append(Person.copy())
        time.sleep(1)
        print(count)
        count+=1

with open('PoliticData.json','w',encoding='utf-8') as f:
    json.dump(Persons,f,indent=4,ensure_ascii=False)