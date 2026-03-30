# -*- coding: utf-8 -*-
"""
AGENTE_ERRO
Detecta erros técnicos de processamento:
- arquivo vazio
- PDF corrompido
- falha de leitura básica
"""

import os
from base_agente import BaseAgente


class AgenteErro(BaseAgente):

    def analisar(self):
        resultado = self._json_base(status="OK")

        # 1) Arquivo inexistente
        if not os.path.exists(self.caminho):
            return self._json_base(
                status="ERRO",
                erro=True,
                motivo="arquivo_nao_encontrado"
            )

        # 2) Arquivo vazio
        tamanho = os.path.getsize(self.caminho)
        if tamanho == 0:
            return self._json_base(
                status="ERRO",
                erro=True,
                motivo="arquivo_vazio"
            )

        # 3) Tentativa mínima de leitura binária
        try:
            with open(self.caminho, "rb") as f:
                header = f.read(5)
                if header != b"%PDF-":
                    return self._json_base(
                        status="ERRO",
                        erro=True,
                        motivo="pdf_invalido"
                    )
        except Exception as e:
            return self._json_base(
                status="ERRO",
                erro=True,
                motivo=f"falha_leitura: {str(e)}"
            )

        # Nenhum erro técnico encontrado
        return resultado