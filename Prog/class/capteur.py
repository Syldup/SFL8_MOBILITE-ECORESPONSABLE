#!/usr/bin/env python3
from threading import Thread
from abc import ABC, abstractmethod

class Capteur(ABC, Thread):
    @abstractmethod
    def __init__(self):
    	Thread.__init__(self)
    	self.value = None
    	self.last_value = None

    @abstractmethod
    def get_value(self):
    	return None
