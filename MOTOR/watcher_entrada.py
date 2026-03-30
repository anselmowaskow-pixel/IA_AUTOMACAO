import time
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from MOTOR.orquestrador import processar_arquivo
from MOTOR.registrador_eventos import registrar_evento
from MOTOR.config import STORAGE_PATH

EXTENSOES_VALIDAS = {".pdf", ".jpg", ".jpeg", ".png", ".xml"}


class EntradaHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return

        caminho = Path(event.src_path)

        if caminho.suffix.lower() not in EXTENSOES_VALIDAS:
            return

        try:
            empresa = caminho.parents[1].name  # STORAGE/Empresa_X/ENTRADA/arquivo
        except IndexError:
            return

        registrar_evento(
            tipo_evento="ENTRADA",
            entidade=empresa,
            arquivo=caminho.name,
            observacao="Arquivo detectado na entrada"
        )

        processar_arquivo(empresa, caminho)


def iniciar_watcher_entrada():
    observer = Observer()
    handler = EntradaHandler()

    for empresa_dir in Path(STORAGE_PATH).iterdir():
        entrada = empresa_dir / "ENTRADA"
        if entrada.exists() and entrada.is_dir():
            observer.schedule(handler, str(entrada), recursive=False)

    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()


if __name__ == "__main__":
    iniciar_watcher_entrada()