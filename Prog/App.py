#!/usr/bin/env python3
from abc import ABC, abstractmethod

class Capteur(ABC):

    @abstractmethod
	def __init__(self):
		pass


if __name__=="__main__":

	capteurs = dict()
	capteurs["gps"] = 