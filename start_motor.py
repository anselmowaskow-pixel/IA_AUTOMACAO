# start_motor.py
import sys
import time
import os
import traceback

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

LOG_DIR = os.path.join(BASE_DIR, "STORAGE", "LOGS")
os.makedirs(LOG_DIR, exist_ok=True)

LOG_FILE = os.path.join(LOG_DIR, "motor.log")

def log(msg):
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(msg + "\n")

def main():
    log("=== MOTOR INICIADO ===")

    try:
        from MOTOR.watcher_entrada import iniciar_watcher

        log("Watcher de ENTRADA carregado")
        iniciar_watcher()

    except Exception as e:
        log("ERRO FATAL NO MOTOR")
        log(str(e))
        log(traceback.format_exc())

        # espera e tenta manter vivo
        time.sleep(10)

if __name__ == "__main__":
    while True:
        main()
        time.sleep(5)