import os
import socket
import subprocess
import sys
import threading
from logging import getLogger
from pathlib import Path
from typing import Literal
import platform
import webbrowser
from argparse import ArgumentParser
from uvicorn import Config, Server

DEFAULT_METHOD_FOR_STARTING_SERVER = "same_terminal"
if platform.system() == "Darwin":
    DEFAULT_METHOD_FOR_STARTING_SERVER = "same_terminal"

if "site-packages/Orange/widgets" in os.path.dirname(os.path.abspath(__file__)).replace("\\", "/") and platform.system() == "Windows":
    DEFAULT_METHOD_FOR_STARTING_SERVER = "new_terminal"


logger = getLogger(__name__)

def is_port_in_use(port: int) -> bool:
    """Check if a port is already in use."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('127.0.0.1', port)) == 0
    

def start_server(port: int = 8000, method: Literal["new_terminal", "same_terminal"] = DEFAULT_METHOD_FOR_STARTING_SERVER) -> None:
    os_type = platform.system()

    if os_type == "Darwin" and method == "new_terminal":
        method = "same_terminal"
        print("Only same_terminal method is supported on macOS. Starting server in the same terminal.")
    print("Start server called with method: ", method)
    if is_port_in_use(port):
        return
    if method == "new_terminal":
        _start_server_in_new_terminal(port)
    elif method == "same_terminal":
        _start_server_in_same_terminal(port)
    else:
        print(f"Invalid method: {method}")


def _start_server_in_new_terminal(port: int = 8000):
    """Starts the server in a new terminal."""
    path_uvicorn="uvicorn"
    if os.name == "darwin":
        raise NotImplementedError("Starting a new terminal is not supported on macOS.")
    if os.name == "nt":
        path_exec = Path(sys.executable)
        path_uvicorn1 = path_exec.parent / "uvicorn.exe" # Henri    
        path_uvicorn2 = path_exec.parent / "Scripts" / "uvicorn.exe" # Lucas

        if not path_uvicorn1.exists() and not path_uvicorn2.exists():
            print("uvicorn not found in the Python path. Please install uvicorn using 'pip install uvicorn'.")
        else:
            if path_uvicorn1.exists():
                path_uvicorn = path_uvicorn1
            else:
                path_uvicorn = path_uvicorn2
                
    command = f"{path_uvicorn} main:app --port {port}"
    path = Path(__file__).parent
    os_type = platform.system()
    if os_type == "Darwin":
        server_process = subprocess.Popen(
            ['open', '-a', 'Terminal', path, '--args', '-c', command]
        )
    else:
        server_process = subprocess.Popen(['cmd', '/c', f'start', 'cmd', '/k', command], cwd=path)


def _start_server_in_same_terminal(port: int = 8000, new_thread=True) -> None:
    """Starts the server in a separate thread."""

    def run_server():
        """Internal function to configure and run the Uvicorn server."""
        upper_folder = Path(__file__).parent.resolve()
        sys.path.append(str(upper_folder))  # Ensure the path is absolute and resolved
        config = Config(app="main:app", port=port)  # Explicitly bind host
        server = Server(config)

        try:
            server.run()
        except Exception as e:
            print(f"Error: {e}")

    # Start the server in a new daemon thread
    if new_thread:
        server_thread = threading.Thread(target=run_server)
        server_thread.start()
        print("Server started on a separate thread.")

    else:
        run_server()


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--port", type=int, default=8000)
    parser.add_argument("--silent_browser", type=bool, default=False)
    args = parser.parse_args()

    
    os.chdir(os.path.dirname(__file__))
    if not args.silent_browser:
        webbrowser.open("http://localhost:8000/docs")
    _start_server_in_same_terminal(new_thread=False, port=args.port)
    # _start_server_in_new_terminal(port=args.port)
    
