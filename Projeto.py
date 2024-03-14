from urllib.request import urlopen
from bs4 import BeautifulSoup
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

#Categories
Array = []
navCat = parsed_html.find('nav', attrs={'class': 'current-category'})
categorias = navCat.find_all('a')
for categoria in categorias:
    Array.append(categoria.get_text())
resposta_final['categories'] = Array
    
#Descrition
divDes = parsed_html.find('div', attrs={'class': 'proddet'})
descricao = divDes.find_all('p')
for desc in descricao:
    resposta_final['description'] = desc.get_text()

#Properties
propi = []
table = parsed_html.find('table', attrs={'class': 'pure-table'})
propiedades = table.find_all('tr')
for propriedade in propiedades:
    label = propriedade.find('b').get_text()
    td_tag = propriedade.find_all('td')[1].get_text()
    propi.append({'label': label, 'value': td_tag})
resposta_final['proprietes'] = propi

#Reviews
reviews = []
avaliacoes = parsed_html.find_all('div', attrs={'class': 'analisebox'})
for avaliacao in avaliacoes:
    review = {}
    review['nome'] = avaliacao.find('span', attrs={'class': 'analiseusername'}).get_text()
    review['date'] = avaliacao.find('span', attrs={'class': 'analisedate'}).get_text()

    estrelas = avaliacao.find('span', attrs={'class': 'analisestars'}).get_text()
    Avestrela = 0
    for i in estrelas:
        if(i == '★'):
            Avestrela += 1
    review['score'] = Avestrela

    review['text'] = avaliacao.find('p').get_text()

    reviews.append(review)
resposta_final['reviews'] = reviews

#URL
link = parsed_html.find('a')
resposta_final['url'] = link.get('href')
# print(link.get('href'))

json_resposta_final = json.dumps(resposta_final, indent=4, ensure_ascii=False)

with open('produto.json', 'w', encoding='utf-8') as arquivo_json:
    arquivo_json.write(json_resposta_final)