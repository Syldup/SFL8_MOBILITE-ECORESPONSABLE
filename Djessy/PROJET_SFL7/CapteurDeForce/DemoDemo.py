#!/usr/bin/python3.4
# coding: utf-8
"""
Programme : Demo BDD
Auteur : L.Burban
Date : 01-03-2019
Matériel utilisé : carte raspberry
Fonction :
    demonstarion de l'utilisation de la lybrary base de données
"""

import sys
sys.path.append('Library/')
from baseDeDonnees import *


MaBDD=BDD("10.16.2.178","SFL7admin","password","basededonneessfl7")
MaBDD.liretable("zone","accident")
MaBDD.liretout("gps")
MaBDD.insererAccident("critique","MON ENORME INTELLIGENCE")
MaBDD.insererCoordoneesGPS("6","9","50k/h",360,"SUD")
