# dev_gestora_pro.py
# DevGestora PRO - supervisao, auditoria e utilitarios de log
# Sem acentos e sem pontuacao especial

import os
import datetime
import json
import threading

# Configuracao
BASE_DIR = r"C:\IA_AUTOMACAO"
LOGS_DIR = os.path.join(BASE_DIR, "LOGS")
LOG_TEXT = os.path.join(LOGS_DIR, "auditoria_pro.txt")
LOG_JSON = os.path.join(LOGS_DIR, "auditoria_pro.json")
TIMEZONE_OFFSET_HOURS = -3  # Brasil horario padrao (UTC-3) -> ajuste se necessario

# Garantir diretorios existentes
os.makedirs(LOGS_DIR, exist_ok=True)

# Lock para escrita concorrente segura no mesmo processo
_write_lock = threading.Lock()

def _now_iso():
    """Retorna timestamp em ISO no fuso configurado"""
    utc = datetime.datetime.utcnow()
    local = utc + datetime.timedelta(hours=TIMEZONE_OFFSET_HOURS)
    return local.replace(microsecond=0).isoformat(sep=" ")

def _append_text(line: str):
    """Escreve uma linha simples no arquivo de texto"""
    try:
        with _write_lock:
            with open(LOG_TEXT, "a", encoding="utf-8") as f:
                f.write(line + "\n")
    except Exception as e:
        # nao pode lançar erro critico aqui; log de erro no console
        print("[DevGestora PRO] Erro ao gravar log texto:", e)

def _append_json(entry: dict):
    """Acrescenta um registro JSON ao arquivo JSON (append line-delimited)"""
    try:
        with _write_lock:
            with open(LOG_JSON, "a", encoding="utf-8") as f:
                f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    except Exception as e:
        print("[DevGestora PRO] Erro ao gravar log json:", e)

def registrar_acao(acao: str, contexto: dict = None):
    """
    Registra uma acao na auditoria.
    - acao: string curta descrevendo a acao
    - contexto: dicionario com dados extras (opcional)
    """
    ts = _now_iso()
    # linha texto padrao
    text_line = f"{ts} - DevGestora_PRO - {acao}"
    if contexto:
        try:
            context_str = json.dumps(contexto, ensure_ascii=False)
            text_line = f"{text_line} - {context_str}"
        except Exception:
            pass

    # objeto json estruturado
    entry = {
        "timestamp": ts,
        "component": "DevGestora_PRO",
        "action": acao,
        "context": contexto or {}
    }

    _append_text(text_line)
    _append_json(entry)
    # feedback leve no console
    print(f"[DevGestora_PRO] {acao}")

def ler_ultimos(n: int = 50):
    """
    Retorna as ultimas n linhas do arquivo de texto como lista de strings.
    Se o arquivo nao existir, retorna lista vazia.
    """
    try:
        if not os.path.exists(LOG_TEXT):
            return []
        with open(LOG_TEXT, "r", encoding="utf-8") as f:
            linhas = f.readlines()
            linhas = [l.rstrip("\n") for l in linhas]
            return linhas[-n:]
    except Exception as e:
        print("[DevGestora_PRO] Erro ao ler auditoria:", e)
        return []

def buscar_json_filtrado(chave: str, valor, max_results: int = 100):
    """
    Busca nos registros JSON por entradas onde entry['context'].get(chave) == valor
    Retorna lista de dicionarios (ate max_results)
    """
    results = []
    try:
        if not os.path.exists(LOG_JSON):
            return results
        with open(LOG_JSON, "r", encoding="utf-8") as f:
            for line in f:
                try:
                    obj = json.loads(line)
                    ctx = obj.get("context", {})
                    if ctx.get(chave) == valor:
                        results.append(obj)
                        if len(results) >= max_results:
                            break
                except Exception:
                    continue
    except Exception as e:
        print("[DevGestora_PRO] Erro na busca JSON:", e)
    return results

def inicializar_gestora():
    """Acao de inicializacao da gestora"""
    registrar_acao("Gestora iniciada")

def finalizar_gestora():
    """Acao de finalizacao da gestora"""
    registrar_acao("Gestora finalizada")

# Ferramenta util para reiniciar logs (nao usada automaticamente)
def limpar_logs():
    try:
        with _write_lock:
            if os.path.exists(LOG_TEXT):
                os.remove(LOG_TEXT)
            if os.path.exists(LOG_JSON):
                os.remove(LOG_JSON)
        print("[DevGestora_PRO] Logs removidos")
    except Exception as e:
        print("[DevGestora_PRO] Erro ao limpar logs:", e)

# Se executado diretamente para teste rapido
if __name__ == "__main__":
    inicializar_gestora()
    registrar_acao("Teste registro direto", {"teste": True})
    print("Ultimos registros:", ler_ultimos(5))
    finalizar_gestora()
