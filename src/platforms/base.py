from abc import ABC, abstractmethod

class PlataformaConsulta(ABC):

    @abstractmethod
    def __init__(self):
        self.website_id = None

    @abstractmethod
    def consultar(self, documento, filtro):
        pass
