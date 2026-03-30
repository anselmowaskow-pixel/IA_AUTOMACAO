import sqlite3
import datetime

# ======================================================
# BANCO
# ======================================================

DB = r"C:\IA_AUTOMACAO\STORAGE\IA_AUTOMACAO.db"


# ======================================================
# GARANTIR TABELAS
# ======================================================

def inicializar_banco():

    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS eventos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        id_evento TEXT,
        data TEXT,
        hora TEXT,
        empresa TEXT,
        arquivo TEXT,
        documento TEXT,
        numero TEXT,
        cpf_emitente TEXT,
        cnpj_emitente TEXT,
        nat_operacao TEXT,
        valor TEXT,
        chave TEXT,
        status TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS decisoes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        data TEXT,
        hora TEXT,
        empresa TEXT,
        arquivo TEXT,
        documento TEXT,
        operacao TEXT,
        status TEXT,
        acao TEXT
    )
    """)

    conn.commit()
    conn.close()


# ======================================================
# REGISTRAR EVENTO
# ======================================================

def registrar_evento(documento):

    agora = datetime.datetime.now()

    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.execute("""
    INSERT INTO eventos (
        id_evento,
        data,
        hora,
        empresa,
        arquivo,
        documento,
        numero,
        cpf_emitente,
        cnpj_emitente,
        nat_operacao,
        valor,
        chave,
        status
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (

        documento.get("id_evento",""),
        agora.strftime("%Y-%m-%d"),
        agora.strftime("%H:%M:%S"),

        documento.get("empresa",""),
        documento.get("arquivo",""),
        documento.get("tipo_documento",""),        # 🔥 corrigido
        documento.get("numero_documento",""),      # 🔥 corrigido

        documento.get("cpf_emitente",""),
        documento.get("cnpj_emitente",""),

        documento.get("natureza_operacao",""),     # 🔥 corrigido
        documento.get("valor_total",""),           # 🔥 corrigido
        documento.get("chave_acesso",""),          # 🔥 corrigido

        documento.get("status","")

    conn.commit()
    conn.close()


# ======================================================
# REGISTRAR DECISAO
# ======================================================

def registrar_decisao(documento, decisao):

    agora = datetime.datetime.now()

    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.execute("""
    INSERT INTO decisoes (
        data,
        hora,
        empresa,
        arquivo,
        documento,
        operacao,
        status,
        acao
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (

        agora.strftime("%Y-%m-%d"),
        agora.strftime("%H:%M:%S"),

        documento.get("empresa",""),
        documento.get("arquivo",""),

        documento.get("documento",""),
        documento.get("nat_operacao",""),

        decisao.get("status",""),
        decisao.get("acao","")

    ))

    conn.commit()
    conn.close()


# ======================================================
# INICIAR
# ======================================================

inicializar_banco()