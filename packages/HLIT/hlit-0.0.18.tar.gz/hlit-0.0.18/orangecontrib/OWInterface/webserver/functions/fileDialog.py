import asyncio
import ctypes
import threading
import os
from starlette.responses import JSONResponse
from typing import Literal, Union
import sys
from AnyQt.QtWidgets import QApplication, QFileDialog


dialog_should_close = threading.Event()


def set_dpi_awareness():
    if os.name == "nt":
        ctypes.windll.shcore.SetProcessDpiAwareness(1)


def open_file_dialog_sync(mode: Literal["file", "folder"]) -> Union[str, list, None]:
    """
    Opens a dialog to select files or a folder based on the mode.

    :param mode: Either "file" (to select files) or "folder" (to select a folder).
    :return: The selected path(s). A string for a folder, a list of strings for files, or None if nothing is selected.
    """
    if mode == "folder":
        return QFileDialog.getExistingDirectory(None, "Select Folder")
    elif mode == "file":
        selected_files, _ = QFileDialog.getOpenFileNames(None, "Select Files")
        return selected_files if selected_files else "!No path selected!"
    else:
        raise ValueError("Invalid mode. Use 'file' or 'folder'.")


async def choose_file_on_server():
    loop = asyncio.get_event_loop()
    path = await loop.run_in_executor(None, open_file_dialog_sync, "file")
    return JSONResponse(content={"path": path})

async def choose_folder_on_server():
    loop = asyncio.get_event_loop()
    path = await loop.run_in_executor(None, open_file_dialog_sync, "folder")
    return JSONResponse(content={"path": path})



# Example Usage
if __name__ == "__main__":
    # Folder selection mode
    selected_folder = open_file_dialog_sync("folder")
    if selected_folder:
        print(f"Selected folder: {selected_folder}")
    else:
        print("No folder selected.")

    # File selection mode
    selected_files = open_file_dialog_sync("file")
    if selected_files:
        print(f"Selected files: {selected_files}")
    else:
        print("No files selected.")