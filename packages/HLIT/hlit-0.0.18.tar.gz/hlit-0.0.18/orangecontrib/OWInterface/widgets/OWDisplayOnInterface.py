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
    name = "Display on Local Interface"
    description = "Push data to a local interface"
    icon = "icons/local_interf_push.svg"
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
    output_fileId: str = Setting('untitled.csv') # type: ignore
    workflow_id: str = Setting('test.ows') # type: ignore
    CSVDelimiter: str = Setting('\t') # type: ignore

    def __init__(self):
        super().__init__()
        self.info_label = gui.label(self.controlArea, self, "Initial info.")
        self.data = None
        self.base_folder = Path(__file__).parent.parent / "webserver" / "received_files"
        self.in_process_queue = self.base_folder / "in_process_queue.json"

        # Ensure the directory and queue file are present
        if not self.in_process_queue.exists():
            self.in_process_queue.parent.mkdir(parents=True, exist_ok=True)
            self.in_process_queue.touch(exist_ok=True)
        self.setup_ui()

    def get_output_folder(self) -> Union[str, None]:
        """Return the output folder for data saving."""
        try:
            with open(self.in_process_queue, 'r') as f:
                in_process_queue = json.load(f)
            
            for item in in_process_queue:
                if item['workflow_id'] == self.workflow_id:
                    return item['output_folder']
                
            raise ValueError("Workflow ID provided does not exist in the queue.")
        
        except json.decoder.JSONDecodeError:
            print("No items in the queue.")
        
        except ValueError:
            # Emit an error message when the workflow ID does not match
            self.Error.upload_failed()
            print("UploadWidget error. Workflow ID provided does not match the workflow id of inputs. Upload failed.")
            self.info_label.setText("UploadWidget error. Workflow ID provided does not match the workflow id of inputs. Upload failed.")

    def setup_ui(self):
        """Set up the user interface."""
        # Text input for fileId
        hbox = gui.hBox(self.controlArea, "File Name")
        self.le_fileId = QLineEdit(self)
        self.le_fileId.setText(self.output_fileId)
        self.le_fileId.editingFinished.connect(self.update_fileId)
        hbox.layout().addWidget(self.le_fileId) # type: ignore

        # Text input for Workflow ID
        hbox2 = gui.hBox(self.controlArea, "Workflow ID")
        self.le_workflow_id = QLineEdit(self)
        self.le_workflow_id.setText(self.workflow_id)
        self.le_workflow_id.editingFinished.connect(self.update_workflow_id)
        hbox2.layout().addWidget(self.le_workflow_id) # type: ignore

        # Text input for CSV delimiter
        hbox3 = gui.hBox(self.controlArea, "CSV Delimiter")
        self.le_csv_delimiter = QLineEdit(self)
        self.le_csv_delimiter.setText(self.CSVDelimiter)
        self.le_csv_delimiter.editingFinished.connect(self.update_csv_delimiter)
        hbox3.layout().addWidget(self.le_csv_delimiter) # type: ignore

        # Button to reset CSV delimiter to \t, as it can't be typed in the text input
        reset_csv_delimiter = gui.button(self.controlArea, self, "Reset Delimiter to \\t", callback=self.reset_csv_delimiter)

        self.adjustSize()
    
    def reset_csv_delimiter(self):
        """Reset the CSV delimiter to \t."""
        self.le_csv_delimiter.setText('\t')
        self.update_csv_delimiter()
    
    def update_csv_delimiter(self):
        """Update the CSV delimiter."""
        self.CSVDelimiter = self.le_csv_delimiter.text()

    @Inputs.data
    def dataset(self, data):
        """Handle new data input."""
        self.data = data
        if self.data is not None:
            self.save_to_file()

    def update_fileId(self):
        """Update the file ID ensuring it has a .csv extension."""
        self.output_fileId = self.ensure_csv_extension(self.le_fileId.text())
    
    def update_workflow_id(self):
        """Update the workflow ID."""
        self.workflow_id = self.le_workflow_id.text()

    def save_to_file(self):
        """Save data to a file."""
        if self.data is None:
            QMessageBox.warning(self, "No Data", "No data available to save.")
            return

        output_folder = self.get_output_folder()
        if output_folder is None:
            print("No file to upload. The queue doesn't contain any item with the provided Workflow ID.")
            return

        file_path = Path(output_folder) / self.output_fileId
        
        try:
            with tempfile.NamedTemporaryFile(delete=False) as temp:
                class CustomReader(CSVReader):
                    DELIMITERS = self.CSVDelimiter
                CustomReader.write(temp.name, self.data)
            os.replace(temp.name, file_path)
            self.info_label.setText(f"Data successfully uploaded")
            print("Data successfully saved to: ", file_path)
        except IOError as err:
            QMessageBox.critical(self, "Error", f"Failed to save file: {err}")

    @staticmethod
    def ensure_csv_extension(fileId: str) -> str:
        """Ensure the file ID ends with a .csv extension."""
        return fileId if fileId.endswith('.csv') else fileId + '.csv'

if __name__ == "__main__": 
    WidgetPreview(OWDisplayOnInterface).run(Table("iris"))
