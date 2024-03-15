from urllib.request import urlopen
from bs4 import BeautifulSoup
import json

url = urlopen("https://infosimples.com/vagas/desafio/commercia/product.html")
parsed_html = BeautifulSoup(url, "html.parser")
resposta_final = {}

def Titulo(): resposta_final['title'] = parsed_html.find('title').get_text()
def Marca(): resposta_final['brand'] = parsed_html.find('div', attrs={'class': 'brand'}).get_text()

def Categorias():
    Array = []
    navCat = parsed_html.find('nav', attrs={'class': 'current-category'})
    categorias = navCat.find_all('a')
    for categoria in categorias: Array.append(categoria.get_text())
    resposta_final['categories'] = Array

def Descricao():
    divDes = parsed_html.find('div', attrs={'class': 'proddet'})
    descricao = divDes.find_all('p')
    for desc in descricao: resposta_final['description'] = desc.get_text()

def Skus():
    Caracteristicas = []
    produtos = parsed_html.find_all('div', attrs={'class': 'card-container'})
    for produto in produtos:
        Caracteristica = {}
        Caracteristica['name'] = produto.find('div', attrs={'class': 'prod-nome'}).get_text()
        preco = produto.find('div', attrs={'class': 'prod-pnow'})
        precoAntigo = produto.find('div', attrs={'class': 'prod-pold'}) 
        temProduto = produto.find('i')

        #Verifica se tem preco
        if preco is None:
            Caracteristica['current-price'] = None
        else:
            Caracteristica['current-price'] = preco.get_text()

        #Verifica o nome antigo
        if precoAntigo is None:
            Caracteristica['old-price'] = None
        else:
            Caracteristica['old-price'] = precoAntigo.get_text()

        #Verifica sem tem no estoque
        if(temProduto):
            Caracteristica['availabe'] = False
        else:
            Caracteristica['availabe'] = True
        
        Caracteristicas.append(Caracteristica)
    resposta_final['Skus'] = Caracteristicas

def Propriedades():
    propi = []
    table = parsed_html.find('table', attrs={'class': 'pure-table'})
    propiedades = table.find_all('tr')
    for propriedade in propiedades:
        label = propriedade.find('b').get_text()
        td_tag = propriedade.find_all('td')[1].get_text()
        propi.append({'label': label, 'value': td_tag})
    resposta_final['proprietes'] = propi

def Reviews():
    reviews = []
    media = 0.0
    totalAvaliacoes = 0
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
        totalAvaliacoes += 1
        media += Avestrela
        review['score'] = Avestrela
        review['text'] = avaliacao.find('p').get_text()
        reviews.append(review)
    resposta_final['reviews'] = reviews
    Media(media, totalAvaliacoes)

def Media(media, totalAv):
    resposta_final['reviews_average_score'] = format(media / totalAv, '.2f')

def URL():
    link = parsed_html.find('a')
    resposta_final['url'] = link.get('href')

Titulo()
Marca()
Categorias()
Descricao()
Skus()
Propriedades()
Reviews()
URL()

json_resposta_final = json.dumps(resposta_final, indent=4, ensure_ascii=False)
with open('produto.json', 'w', encoding='utf-8') as arquivo_json:
    arquivo_json.write(json_resposta_final)