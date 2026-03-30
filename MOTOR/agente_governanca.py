# agente_governanca.py
# AGENTE DE GOVERNANCA - DECISAO DE RESPONSABILIDADE

class AgenteGovernanca:

    def decidir(self, evento):
        status = evento.get("status")

        if status == "OK":
            return self._decisao(
                destino="CONTADOR",
                acao="ENCAMINHAR",
                motivo="Documento pronto para validacao fiscal"
            )

        if status == "ERRO":
            return self._decisao(
                destino="EMPRESA",
                acao="AJUSTAR",
                motivo="Erro tecnico corrigivel"
            )

        if status == "ERRO_ILEGIVEL":
            return self._decisao(
                destino="CONTADOR",
                acao="ANALISE_MANUAL",
                motivo="Documento ilegivel"
            )

        if status == "DUPLICADO":
            return self._decisao(
                destino="CONTADOR",
                acao="DECIDIR_DUPLICIDADE",
                motivo="Duplicidade exige decisao contabil"
            )

        return self._decisao(
            destino="EMPRESA",
            acao="AGUARDAR",
            motivo="Status desconhecido"
        )

    def _decisao(self, destino, acao, motivo):
        return {
            "destino": destino,
            "acao": acao,
            "motivo": motivo
        }

    def detectar_fornecedor_novo(cnpj, eventos):

        fornecedores = set()

        for evento in eventos:
            fornecedores.add(evento["cnpj"])

        if cnpj not in fornecedores:
            return True

        return False    