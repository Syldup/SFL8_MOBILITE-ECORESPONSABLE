#!/usr/bin/env python3
from abc import ABC, abstractmethod

class Capteur(ABC):
    @abstractmethod
    def __init__(self):
        self.value = None
        self.last_value = None

    @abstractmethod
    def get_value(self):
        return None
