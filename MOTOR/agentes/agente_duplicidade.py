# agente_duplicidade.py
# AGENTE CANONICO DE DUPLICIDADE POR HASH

import os
import hashlib
import csv

from base_agente import BaseAgente
from config import EVENTOS_CSV


class AgenteDuplicidade(BaseAgente):
    NOME = "AGENTE_DUPLICIDADE"

    def executar(self):
        hash_atual = self._hash_arquivo(self.caminho)

        if not os.path.exists(EVENTOS_CSV):
            return self._json_ok(hash_atual)

        with open(EVENTOS_CSV, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for linha in reader:
                if linha.get("hash") == hash_atual:
                    return self._json_erro(
                        status="DUPLICADO",
                        mensagem="Arquivo duplicado por hash",
                        hash_documento=hash_atual
                    )

        return self._json_ok(hash_atual)

    def _hash_arquivo(self, caminho):
        h = hashlib.sha256()
        with open(caminho, "rb") as f:
            for chunk in iter(lambda: f.read(8192), b""):
                h.update(chunk)
        return h.hexdigest()

    def _json_ok(self, hash_documento):
        return {
            "status": "OK",
            "hash": hash_documento
        }

    def _json_erro(self, status, mensagem, hash_documento):
        return {
            "status": status,
            "mensagem": mensagem,
            "hash": hash_documento
        }