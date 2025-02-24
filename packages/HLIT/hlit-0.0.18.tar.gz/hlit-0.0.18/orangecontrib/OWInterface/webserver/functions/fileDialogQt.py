import asyncio
import ctypes
import os
import threading
import time
from starlette.responses import JSONResponse


from AnyQt.QtWidgets import QFileDialog

dialog_should_close = threading.Event()

def set_dpi_awareness():
    if os.name == "nt":
        ctypes.windll.shcore.SetProcessDpiAwareness(1)

def open_file_dialog_sync():
    set_dpi_awareness()

    # Utilisation de QFileDialog.getOpenFileNames pour sélectionner plusieurs fichiers
    filepaths, _ = QFileDialog.getOpenFileNames(None, "Select files", "", "All Files (*)")

    if filepaths:
        print("Selected files:")
        for path in filepaths:
            print(path)
        return filepaths
    else:
        print("No file selected.")
        return ()

async def choose_file_on_server():
    loop = asyncio.get_event_loop()
    filepaths = await loop.run_in_executor(None, open_file_dialog_sync)
    return JSONResponse(content={"filepaths": filepaths})
