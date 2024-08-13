import numpy as np
#"Place;Temps;Nom;Nationalité;Genre;Catégorie;Score\n"
class utmbData:
    Nationalite=["Nationalites",[]]
    Genre=["Genres",[]]
    Categorie=["Categories",[]]
    data=[]
    dataAnalysed=[]
    
    def __init__(self, data):
        for d in data:
            if len(d)==7:
                #Donnees correctes on ajoute a la liste
                self.data.append(d)
                
                # Add unique nationalities
                if d[3] not in self.Nationalite[1]:
                    self.Nationalite[1].append(d[3])
                
                # Add unique genres
                if d[4] not in self.Genre[1]:
                    self.Genre[1].append(d[4])
                
                # Add unique categories
                if d[5] not in self.Categorie[1]:
                    self.Categorie[1].append(d[5])
        return

    def analyseGlobale(self):       
       
        #Analyse totale
        self.dataAnalysed.append(["Analyse totale",self.analyseTotale()])
        #Analyse par nationalité
        self.dataAnalysed.append(["Analyse par nationalite",self.analyseParNationalite()])
        #Analyse par nationalité et catégorie
        self.dataAnalysed.append(["Analyse par nationalite et categorie",self.analyseParNationaliteEtCategorie()])
        #Analyse par genre
        self.dataAnalysed.append(["Analyse par genre",self.analyseParGenre()])
        #Analyse par genre et catégorie
        self.dataAnalysed.append(["Analyse par genre et categorie",self.analyseParGenreEtCategorie()])
        #Analyse par Nationalité genre et catégorie
        self.dataAnalysed.append(["Analyse par nationalite, genre et categorie", self.analyseParNationaliteGenreEtCategorie()])
     
        return self

    def analyseTotale(self):
        value=[]
        for d in self.data:
            if isinstance(d[6], int):
                value.append(d[6])
        return [self.analyseData("tous","tous","tous",value)]
    
    def analyseParNationalite(self):
        t=[]
        for nation in self.Nationalite[1]:
            dataParNationalite=[]
            for d in self.data:
                if d[3]==nation and isinstance(d[6], int):
                    dataParNationalite.append(d[6])
            if dataParNationalite:
                t.append(self.analyseData(nation,"tous","tous",dataParNationalite))
        return t
    

    
    def analyseParGenre(self):
        t=[]
        for genre in self.Genre[1]:
            dataParGenre=[]
            for d in self.data:
                if d[4]==genre and isinstance(d[6], int):
                    dataParGenre.append(d[6])
            if dataParGenre:
                t.append(self.analyseData("tous","tous",genre,dataParGenre))
        return t
        
        

    def analyseParGenreEtCategorie(self):
        t=[]
        for genre in self.Genre[1]:
            for categorie in self.Categorie[1]:
                dataParGenre=[]
                for d in self.data:
                    if d[4]==genre and d[5]==categorie and isinstance(d[6], int):
                        dataParGenre.append(d[6])
                if dataParGenre:
                    t.append(self.analyseData("tous",genre,categorie,dataParGenre))
        return t
    
    def analyseParNationaliteEtCategorie(self):
        t=[]
        for nationalite in self.Nationalite[1]:
            for categorie in self.Categorie[1]:
                dataParNationalite=[]
                for d in self.data:
                    if d[3]==nationalite and d[5]==categorie and isinstance(d[6], int):
                        dataParNationalite.append(d[6])
                if dataParNationalite:
                    t.append(self.analyseData(nationalite,"tous",categorie,dataParNationalite))
        return t

    def analyseParNationaliteGenreEtCategorie(self):
        t=[]
        for nationalite in self.Nationalite[1]:
            for genre in self.Genre[1]:
                for categorie in self.Categorie[1]:
                    dataParNationalite=[]
                    for d in self.data:
                        if d[3]==nationalite and d[4]==genre and d[5]==categorie and isinstance(d[6], int):
                            dataParNationalite.append(d[6])
                    if dataParNationalite:
                        t.append(self.analyseData(nationalite,genre,categorie,dataParNationalite))
        return t

    
    
    
    
    def analyseData(self,nationalite,genre,categorie,data):
             
        dataAnalysees=[nationalite,genre,categorie]
        
        #Nombre
        dataAnalysees.append(len(data))
        #Moyenne
        dataAnalysees.append(np.round(np.mean(data)).astype(int))
        #Mediane
        dataAnalysees.append(np.round(np.median(data)).astype(int))
        #Ecart type
        dataAnalysees.append(np.round(np.std(np.array(data))).astype(int))
        #Repartition centile
        for value in np.round(np.percentile(data, np.arange(0, 100, 1))).astype(int):
            dataAnalysees.append(value)
    
        return dataAnalysees