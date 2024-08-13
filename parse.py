import requests
import math
import analyse
import csv
import os
from bs4 import BeautifulSoup
import numpy as np

def generale(p_lienWeb, utmbIndexMax):
    # create session
    session = requests.Session()
    
    return analyseCourse(p_lienWeb,session, utmbIndexMax)
                    
            
    


def analyseCourse(p_lienWeb,sessionHandler, utmbIndexMax):
    resultats=[]
    titre=""
    #Récupérer la page entrer en parametre
    print("Analyse de la course: "+p_lienWeb)
    soup=getPage(p_lienWeb,sessionHandler)
    if(soup==-1):
        return -1
    else:
    # Find and print the title of the webpage
        titre = soup.find('title').get_text()
        print('Nom de la course : ', titre)


    #Récupérer nombre de pages de résultats
    nbPage=getNbPage(soup)
    if(nbPage==-1):
        print("Erreur impossible de calculer le nombre de page de résultats")
        return -1
    print(f"Il y a { nbPage} pages de résultats de résultats")
    
    #Récupérer les résultats de chaque page
    for i in range(1, nbPage+1):
        urlPageResultat=f"{p_lienWeb.split('?')[0]}?page={i}"
        analysePage(urlPageResultat,resultats,sessionHandler)
    generateUTMBIndex(resultats,utmbIndexMax)
    
    dataAnalysees=analyse.utmbData(resultats).analyseGlobale()

    
    saveData(titre, resultats, dataAnalysees,p_lienWeb)
    return 1

def analysePage(urlPageResultat, resultats,sessionHandler):
    print(f"Analyse de la page: {urlPageResultat}")
    soup=getPage(urlPageResultat,sessionHandler)
    partipants=soup.find('div',  class_='race-table_rt_table__Zoujg my-table_container__4fAnT')
    partipants=list(partipants)
    for participant in partipants[1:]:
        resultats.append(analyseParticipant(str(participant)))
    return

def analyseParticipant(html):    
    soup = BeautifulSoup(html, 'html.parser')

    # Trouver la ligne du tableau
    row = soup.find('div', class_='my-table_row__nlm_j')
    
    # Initialiser un tableau
    data = [""]*7

    # Extraire chaque colonne de la ligne
    columns = row.find_all('div', class_='my-table_cell__z__zN')

    # Analyser chaque colonne et stocker les valeurs dans le dictionnaire
    if columns:
        data[0] = columns[0].text.strip() if len(columns) > 0 else None
        data[1] = columns[1].text.strip() if len(columns) > 1 else None
        data[2] = columns[2].text.strip() if len(columns) > 2 else None
        data[3] = columns[3].find_all('span')[1].text.strip() if len(columns) > 3 else None
        data[4] = columns[4].text.strip() if len(columns) > 4 else None
        data[5] = columns[5].text.strip() if len(columns) > 5 else None
        data[6]=0

    return data

#OK
def getPage(p_lienWeb,sessionHandler):
    if(sessionHandler):
        # Fetch the webpage
        response = sessionHandler.get(p_lienWeb,cookies=sessionHandler.cookies)

        # Check if the request was successful
        if response.status_code == 200:
        # Parse the HTML content
            return BeautifulSoup(response.content, 'html.parser')
        else:
            return -1
        
#OK
def getNbPage(soup):
    target_ul = soup.find('ul', class_='pagination_paginate_container__As8CJ')

    if target_ul:
       # Find all <li> elements within the <ul>
       ln=len(target_ul.find_all('li'))
       #print(target_ul.find_all('li')[ln-1])

       html_code=str(target_ul.find_all('li')[ln-2])
       
       # Créer un objet BeautifulSoup
       soup = BeautifulSoup(html_code, 'html.parser')
       
       # Trouver le lien avec la classe spécifiée
       page_link = soup.find('a', class_='pagination_paginate_link__c9A6i')
       
       # Récupérer la valeur de l'attribut href
       return int(page_link['href'].split('=')[-1])
       
    return -1

def saveData(titre, data, c_dataAnalysees:analyse.utmbData,p_lienWeb):    
    with open(f'{titre}_raw_data.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile, delimiter=';')
        writer.writerow([p_lienWeb])
        writer.writerow("")
        
        criteres=["Place", "Temps", "Nom", "Nationalité", "Genre", "Catégorie", "Score"]
        for i in np.arange(0, 1.05, 0.05):
            criteres.append(i)
        writer.writerow(criteres)
        writer.writerows(data)
        
    with open(f'{titre}_analysed_data.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile, delimiter=';')
        writer.writerow([p_lienWeb])
        writer.writerow("")
        
        c_dataAnalysees.Nationalite[1].insert(0,c_dataAnalysees.Nationalite[0])
        writer.writerow(c_dataAnalysees.Nationalite[1])
        
        c_dataAnalysees.Genre[1].insert(0,c_dataAnalysees.Genre[0])
        writer.writerow(c_dataAnalysees.Genre[1])
        
        c_dataAnalysees.Categorie[1].insert(0,c_dataAnalysees.Categorie[0])
        writer.writerow(c_dataAnalysees.Categorie[1])
        writer.writerow("")
        
        titres=["Nationalite", "Genre", "Categorie", "Nombre", "Moyenne", "Mediane"]      
        for i in np.arange(0, 1.01, 0.01):
            titres.append("Percentile " + f"{i:.2f}")
        
        writer.writerow(titres)
        tmp=c_dataAnalysees.dataAnalysed
        for data in tmp:
            for d in data[1]:
                writer.writerow(d)
    
    return


'''
def saveData(titre, data, dataAnalysees):
    with open(f"{titre}.csv", 'w', encoding='utf-8') as fichier:
        fichier.write("Place;Temps;Nom;Nationalité;Genre;Catégorie;Score\n")
        for i in data:
            string=i[0]
            for j in i[1:]:
                string= string +";"+str(j)
            fichier.write(f"{string}\n")
    return
'''

# Faire l'arrondi >=.29
def generateUTMBIndex(resultats,utmbIndexMax):
    tMin=float(transformeEnSecondes(resultats[0][1]))*float(utmbIndexMax)/1000
    for i in range(len(resultats)):
        if transformeEnSecondes(resultats[i][1])==-1:
            resultats[i][6]=resultats[i][0]
        else:
            #resultats[i][6]=math.ceil(tMin/transformeEnSecondes(resultats[i][1])*1000 - 0.29)
            resultats[i][6]=math.ceil(tMin/transformeEnSecondes(resultats[i][1])*1000-0.5)

    
    return resultats

def transformeEnSecondes(valeur):
    # Diviser la chaîne de caractères en heures, minutes et secondes
    try:
        h, m, s = map(int, valeur.split(':'))
        # Convertir en secondes
        return h * 3600 + m * 60 + s
    except:
        return -1