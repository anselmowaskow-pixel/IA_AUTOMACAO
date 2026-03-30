# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod
from datetime import datetime

class BaseAgente(ABC):
    def __init__(self, entidade, arquivo, caminho_arquivo):
        self.entidade = entidade
        self.arquivo = arquivo
        self.caminho_arquivo = caminho_arquivo
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    @abstractmethod
    def executar(self):
        """
        Deve retornar um JSON canônico no formato:
        {
            "agente": "NOME_DO_AGENTE",
            "entidade": "...",
            "arquivo": "...",
            "status": "OK | DUPLICADO | ERRO | ILEGIVEL | ANALISAR",
            "mensagem": "...",
            "data": "YYYY-MM-DD HH:MM:SS"
        }
        """
        pass