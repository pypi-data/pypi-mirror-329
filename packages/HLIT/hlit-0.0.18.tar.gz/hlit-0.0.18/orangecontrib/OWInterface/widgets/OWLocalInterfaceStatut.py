import os
import json
import tempfile
from pathlib import Path
from typing import Union
from AnyQt.QtWidgets import QLineEdit, QMessageBox
from Orange.data.table import Table
from Orange.widgets import widget, gui
from Orange.widgets.widget import Input
from Orange.widgets.settings import Setting
from Orange.widgets.utils.widgetpreview import WidgetPreview
from Orange.data.io import CSVReader


class OWDisplayOnInterface(widget.OWWidget):
    name = "Upload Statut"
    description = "Push statut to a local interface"
    if "site-packages/Orange/widgets" in os.path.dirname(os.path.abspath(__file__)).replace("\\", "/"):
        icon = "icons_dev/local_interf_push.svg"

    priority = 1220
    category = "Advanced Artificial Intelligence Tools"
    want_main_area = False
    resizing_enabled = False

    class Inputs:
        data = Input("Data", Table)

    # Define an Error class for error messaging
    class Error(widget.OWWidget.Error):
        upload_failed = widget.Msg("Workflow ID does not match inputs. Upload failed.")

    # Persistent settings for fileId and workflow_id
    workflow_id: str = Setting('test.ows') # type: ignore
    messageStatut: str = Setting('') # type: ignore

    def __init__(self):
        super().__init__()
        self.info_label = gui.label(self.controlArea, self, "Initial info.")
        self.message_sta
        self.data = None
        self.base_folder = Path(__file__).parent.parent / "webserver" / "received_files"
        self.in_process_queue = self.base_folder / "in_process_queue.json"

        # Ensure the directory and queue file are present
        if not self.in_process_queue.exists():
            self.in_process_queue.parent.mkdir(parents=True, exist_ok=True)
            self.in_process_queue.touch(exist_ok=True)
        self.setup_ui()

    def get_output_folder(self) -> str:
        """Return the output folder for data saving."""
        try:
            with open(self.in_process_queue, 'r') as f:
                in_process_queue = json.load(f)
            
            for item in in_process_queue:
                if item['workflow_id'] == self.workflow_id:
                    return item['output_folder']
                
            raise ValueError("Workflow ID provided does not exist in the queue.")
        
        
        except ValueError:
            # Emit an error message when the workflow ID does not match
            self.Error.upload_failed()
            print("UploadWidget error. Workflow ID provided does not match the workflow id of inputs. Upload failed.")
            self.info_label.setText("UploadWidget error. Workflow ID provided does not match the workflow id of inputs. Upload failed.")
            raise ValueError("Workflow ID provided does not exist in the queue.")

    def setup_ui(self):
        """Set up the user interface."""

        # Text input for Workflow ID
        hbox2 = gui.hBox(self.controlArea, "Workflow ID")
        self.le_workflow_id = QLineEdit(self)
        self.le_workflow_id.setText(self.workflow_id)
        self.le_workflow_id.editingFinished.connect(self.update_workflow_id)
        hbox2.layout().addWidget(self.le_workflow_id) # type: ignore

        # Text input for statut to upload
        hbox3 = gui.hBox(self.controlArea, "MessageStatut to Upload")
        self.le_message_statut = QLineEdit(self)
        self.le_message_statut.setText(self.messageStatut)
        self.le_message_statut.editingFinished.connect(self.update_message_statut)
        hbox3.layout().addWidget(self.le_message_statut) # type: ignore

        self.adjustSize()


    def update_message_statut(self):
        """Update the message statut."""
        self.messageStatut = self.le_message_statut.text()

    @Inputs.data
    def dataset(self, data):
        """Handle new data input."""
        statut_path_str = Path(self.get_output_folder()) / "__statut__.txt"
            
    
    def update_workflow_id(self):
        """Update the workflow ID."""
        self.workflow_id = self.le_workflow_id.text()



if __name__ == "__main__": 
    pass
    # TODO: Implement a test for this widget.
