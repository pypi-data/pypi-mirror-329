from Orange.widgets import widget, gui, settings
from Orange.data import Table
from pathlib import Path
import json
import os

if "site-packages/Orange/widgets" in os.path.dirname(os.path.abspath(__file__)).replace("\\", "/"):
    from Orange.widgets.orangecontrib.AAIT.download.FileWatcher import FileWatcher
    from Orange.widgets.orangecontrib.AAIT.webserver.start_server import start_server
else:
    from orangecontrib.OWInterface.download.FileWatcher import FileWatcher
    from orangecontrib.OWInterface.webserver.start_server import start_server

class BaseLocalInterfaceWidget(widget.OWWidget, openclass=True):
    # Common settings across all widgets
    workflow_id = settings.Setting("default.ows")  # type: ignore
    input_id = settings.Setting("default_id")  # type: ignore

    class Outputs:
        data = widget.Output("Data", Table)

    def __init__(self):
        super().__init__()
        # GUI elements common to all widgets
        self.info_label = gui.label(self.controlArea, self, "Initial info.")
        self.workflow_id_edit = gui.lineEdit(self.controlArea, self, "workflow_id",
                                             label="Workflow ID:", orientation="horizontal")
        self.input_id_edit = gui.lineEdit(self.controlArea, self, "input_id",
                                         label="input ID:", orientation="horizontal")
        
        # Set up file watcher for all widgets
        self.queue_file_path = self.setup_paths()
        self.file_watcher = FileWatcher(str(self.queue_file_path))
        self.file_watcher.file_modified.connect(self.process_queue)
        # Start server for all widgets
        start_server()
        self.process_queue()

    def setup_paths(self) -> Path:
        # Set default path, can be overridden in derived class if needed
        return Path(__file__).parent.parent / "webserver" / "received_files" / "in_process_queue.json"
    
        
        
    
    def get_files_to_process(self, entry) -> list[Path]:
        try:
            self.opening_method
        except AttributeError:
            raise NotImplementedError("Derived classes must give a value for the attribute 'opening_method'.")
        
        if entry.get("workflow_id") != self.workflow_id:
            return []
        
        file_to_process = []
        for file_entry in entry.get("file_entries", []):
            if file_entry.get("file_id") == self.input_id \
                and file_entry.get("opening_method") == self.opening_method:
                file_path = Path(file_entry["input_filename"])
                if file_path.exists():
                    file_to_process.append(file_path)
                else:
                    self.info_label.setText(f"File not found: {str(file_path)}")
                    print("file not found: ", str(file_path))

        return file_to_process
    


    def process_queue(self) -> None:
        # Standard queue processing logic
        if not self.queue_file_path.exists():
            self.info_label.setText("Queue file not found.")
            return

        try:
            with open(self.queue_file_path, 'r') as queue_file:
                content = queue_file.read().strip()
                if not content:
                    self.info_label.setText("Queue file is empty.")
                    return
                files_to_process = json.loads(content)
        except Exception as e:
            self.info_label.setText(f"Error reading queue file: {e}")


        entries_to_process = [entry for entry in files_to_process if entry.get("workflow_id") == self.workflow_id]
        assert len(entries_to_process) <= 1, "Multiple entries found for a single workflow ID."
        if entries_to_process:
            files_to_process = self.get_files_to_process(entries_to_process[0])
            self.process_files(files_to_process)
            

    def process_files(self, files_to_process: list[Path]):
        # To be implemented in derived classes
        raise NotImplementedError("Derived classes from BaseDownloadWidget must implement the process_entry method.")