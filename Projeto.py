from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import json
# import requests

# url = 'https://infosimples.com/vagas/desafio/commercia/product.html'
url = urlopen("https://infosimples.com/vagas/desafio/commercia/product.html")
parsed_html = BeautifulSoup(url, "html.parser")

resposta_final = {}

# parsed_html = BeautifulSoup(response.content, 'html.parser')
# resposta_final['title'] = parsed_html.select_one('h2#product_title').get_text()

#Titulo
resposta_final['title'] = parsed_html.find('title').get_text()

#Marca do produto
resposta_final['brand'] = parsed_html.find('div', attrs={'class': 'brand'}).get_text()

#Descrition
divDes = parsed_html.find('div', attrs={'class': 'proddet'})
descricao = divDes.find_all('p')
for desc in descricao:
    resposta_final['description'] = desc.get_text()

#Properties
propi = []
padrao = re.compile(r'<td>(.*?)</td>')
table = parsed_html.find('table', attrs={'class': 'pure-table'})
propiedades = table.find_all('tr')
for propriedade in propiedades:
    label = propriedade.find('b').get_text(strip=True)



    # value = propriedade.find('td').get_text(strip=True)
    resultado = re.findall(padrao, propriedade.find('td').get_text())
    


    propi.append({'label': label})
    # propi.append({'value': value})


print(type(value))
resposta_final['proprietes'] = propi

json_resposta_final = json.dumps(resposta_final, indent=4, ensure_ascii=False)

with open('produto.json', 'w', encoding='utf-8') as arquivo_json:
    arquivo_json.write(json_resposta_final)