from abc import ABC, abstractmethod

class PlataformaConsulta(ABC):
    @abstractmethod
    def consultar(self, documento, filtro):
        pass
