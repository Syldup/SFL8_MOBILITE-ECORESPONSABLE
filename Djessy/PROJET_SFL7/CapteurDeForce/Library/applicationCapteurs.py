#!/usr/bin/python3.4
# coding: utf-8
"""
Programme : Application capteur
Auteur : L.Burban
Date : 05-03-2019
Matériel utilisé : capteur de force FSR 400 series
Fonction :
    Convertie une tension d'entrée en une tension nul qui augmente en fonction de la force appliquer sur le capteur et
    la renvoie 
"""
from raspiomix import Raspiomix
from baseDeDonnees import BDD

MaBDD=BDD("10.16.2.178","SFL7admin","password","basededonneessfl7")

r = Raspiomix()

class capteurDeForces:
    def __init__(self,numero,position):
        self.numero = numero
        self.position = position
        
    def lancerCapture(self):
        """ lance la capture du capteur et la renvoie"""
        tension =r.readAdc(self.numero)
        print(tension)
        if tension > 1 and tension < 2 :
            MaBDD.insererAccident("choc faible","%s"%(self.position))
        if tension >= 2 and tension < 3 :
            MaBDD.insererAccident("choc moyen","%s"%(self.position))
        if tension >= 3 and tension < 4 :
            MaBDD.insererAccident("choc fort","%s"%(self.position))
        if tension >= 4 :
            MaBDD.insererAccident("choc critique","%s"%(self.position))
    def lireEnBoucle(self):
        """lit les données du capteur
        /!\ ne renvoie aucune données !"""
        while 1:
            print("La tension en %s est de %f Volt !" % (r.readAdc(self.numero),self.position))

    