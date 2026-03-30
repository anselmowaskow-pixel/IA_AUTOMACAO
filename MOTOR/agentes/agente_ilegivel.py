# -*- coding: utf-8 -*-
from base_agente import BaseAgente
import os
import json
import hashlib

class AgenteIlegivel(BaseAgente):
    """
    Detecta PDFs ilegíveis usando heurísticas simples e robustas:
    - tamanho muito pequeno
    - ausência de texto extraível (placeholder)
    - nome indicando erro/scan ruim
    """

    LIMIAR_BYTES = 8 * 1024  # 8 KB (ajuste fino depois)

    def _hash(self, caminho):
        h = hashlib.sha256()
        with open(caminho, "rb") as f:
            for chunk in iter(lambda: f.read(8192), b""):
                h.update(chunk)
        return h.hexdigest()

    def analisar(self):
        caminho = self.caminho
        nome = os.path.basename(caminho)

        motivos = []

        try:
            tamanho = os.path.getsize(caminho)
            if tamanho < self.LIMIAR_BYTES:
                motivos.append("arquivo_muito_pequeno")

            # Heurística por nome (rápida e prática)
            nome_upper = nome.upper()
            if any(k in nome_upper for k in ["ILEGIVEL", "SCAN", "BORRADO", "RUIM"]):
                motivos.append("indicacao_no_nome")

            # Placeholder para OCR/texto (sem dependências agora)
            # Futuro: integrar OCR real e medir texto extraível
            texto_extraivel = False
            if not texto_extraivel:
                motivos.append("sem_texto_extraivel")

            ilegivel = len(motivos) >= 2  # regra simples e segura

            resultado = {
                "agente": "ilegivel",
                "entidade": self.entidade,
                "arquivo": nome,
                "hash": self._hash(caminho),
                "ilegivel": ilegivel,
                "motivos": motivos,
                "timestamp": self.timestamp
            }

            return resultado

        except Exception as e:
            return {
                "agente": "ilegivel",
                "entidade": self.entidade,
                "arquivo": nome,
                "erro": str(e),
                "timestamp": self.timestamp
            }