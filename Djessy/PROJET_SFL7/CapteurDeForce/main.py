#!/usr/bin/python3.4
# coding: utf-8
"""
Programme : Application lecture capteur
Auteur : L.Burban
Date : 29-01-2019
Matériel utilisé : carte raspberry, capteur de force FSR 400 series
Fonction :
    Convertie une tension d'entrée en une tension nul qui augmente en fonction de la force appliquer sur le capteur et
    la renvoie sur une base de données
"""
import sys
sys.path.append('Library/')
from applicationCapteurs import capteurDeForces
from baseDeDonnees import BDD
import time


capteurDos = capteurDeForces(0,"dos")
capteurTorse = capteurDeForces(4,"torse")
capteurEpauleGauche = capteurDeForces(1,"Epaule Gauche")
capteurEpauleDroite = capteurDeForces(5,"Epaule droite")
capteurBrasGauche = capteurDeForces(2,"Bras gauche")
capteurBrasDroit = capteurDeForces(6,"Bras droit")
capteurFlancGauche = capteurDeForces(3,"Flan gauche")
capteurFlancDroit = capteurDeForces(7,"Flan droite")

while 1:
    capteurDos.lancerCapture()
##    capteurTorse.lancerCapture()
##    capteurEpauleGauche.lancerCapture()
##    capteurEpauleDroite.lancerCapture()
##    capteurBrasGauche.lancerCapture()
##    capteurBrasDroit.lancerCapture()
##    capteurFlancGauche.lancerCapture()
##    capteurFlancDroit.lancerCapture()
