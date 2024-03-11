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

#Categories
divCat = parsed_html.find('div', attrs={'class': 'proddet'})
resposta_final['categories'] = divCat.find("h5")

json_resposta_final = json.dumps(resposta_final)

with open('produto.json', 'w') as arquivo_json:
    arquivo_json.write(json_resposta_final)