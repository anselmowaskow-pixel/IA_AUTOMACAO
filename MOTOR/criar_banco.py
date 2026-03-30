import sqlite3

caminho = r"C:\IA_AUTOMACAO\STORAGE\IA_AUTOMACAO.db"

conn = sqlite3.connect(caminho)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS eventos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    data TEXT,
    hora TEXT,
    empresa TEXT,
    documento TEXT,
    operacao TEXT,
    valor REAL,
    status TEXT,
    acao TEXT,
    arquivo TEXT,
    chave TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS decisoes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    data TEXT,
    hora TEXT,
    empresa TEXT,
    documento TEXT,
    operacao TEXT,
    status TEXT,
    acao TEXT,
    arquivo TEXT
)
""")

conn.commit()
conn.close()

print("BANCO IA_AUTOMACAO CRIADO COM SUCESSO")