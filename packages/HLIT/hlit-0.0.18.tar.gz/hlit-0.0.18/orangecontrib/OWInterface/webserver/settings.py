from pathlib import Path
from functions.fileQueue import FileQueue
import requests

# Path settings
save_directory: Path = Path(__file__).parent / "received_files"
output_directory: Path = Path(__file__).parent / "sent_files"
workflow_directory: Path = Path(__file__).parent / "available_workflows"
html_examples_directory = Path(__file__).parent / "html_examples"


# Name of the final file of a workflow, containing status:
FINAL_FILE_NAME: str = "done"
FINAL_FOLDER_ARCHIVE_NAME: str = "output.zip"

# FileQueues
waiting_queue: FileQueue = FileQueue(save_directory / "waiting_queue.json")
in_process_queue: FileQueue = FileQueue(save_directory / "in_process_queue.json")

# Constants
MAX_PROCESSING_QUEUE_LENGTH: int = 1
TIMEOUT_LIMIT: int = 10  # seconds

# Server descriptions / names

SERVER_NAME: str = "AAIT Widgets Webserver"
EXAMPLE_FOLDER = Path(__file__) / "html_examples"
SERVER_DESCRIPTION: str = f"""
##   Introduction
The purpose of Orange's Download/Upload widgets is to facilitate communication between a remote client and an Orange-hosted server using FastAPI. This setup allows for:

1. Centralization of resource-intensive requests on a single server for clients that do not have a GPU. By offloading heavy computational tasks to the server, clients with limited hardware capabilities can still perform complex operations efficiently.

2. Creation of more user-friendly web interfaces than those available in Orange, which can be accessed via a web browser. This enhances user accessibility and interaction, as the workflow is executed in the background process. The operations occur seamlessly without any visible or modifiable elements for the user, improving the user experience by abstracting complex processes.

This page is the documentation of the AAIT Widgets Webserver. It is designed with fastAPI, to allows the communication between the Orange widgets and the server. The server is able to receive files, process them and send them back to the client.

The full documentation can be accessed here: <br>
<a href="https://github.com/jcmhk/AAIT/blob/dev/documentation_ifia/8_html/WidgetsOrange.md" target="_blank">Git Documentation</a>

All routes can be tested here, and description should be self-explanatory. If not, contact henri.dandria@institut-ia.com
You can see a list of already implemented examples here: <br>
<a href="html_examples/" target="_blank">List of implemented examples</a>
"""






