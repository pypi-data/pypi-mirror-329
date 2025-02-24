import json
import os
from pathlib import Path
from pprint import pprint
from typing import List

import numpy as np
from AnyQt.QtCore import QFileSystemWatcher, QObject, pyqtSignal
from AnyQt.QtGui import QImageReader
from Orange.data import ContinuousVariable, Domain, StringVariable, Table
from Orange.widgets import gui, settings, widget
from Orange.widgets.utils.signals import Output

if "site-packages/Orange/widgets" in os.path.dirname(os.path.abspath(__file__)).replace("\\", "/"):
    from Orange.widgets.orangecontrib.AAIT.download.BaseLocalInterfaceWidget import BaseLocalInterfaceWidget
else:
    from orangecontrib.OWInterface.download.BaseLocalInterfaceWidget import BaseLocalInterfaceWidget


class OWLocalInterfaceImages(BaseLocalInterfaceWidget): # type: ignore
    name = "Local Interface - Images"
    description = ("Monitors a JSON queue file for image paths associated "
                   "with specific workflow and file IDs, and processes images.")
    icon = "icons/local_interf_img_multi_pull.svg"
    if "site-packages/Orange/widgets" in os.path.dirname(os.path.abspath(__file__)).replace("\\", "/"):
        icon = "icons_dev/local_interf_img_multi_pull.svg"
    priority = 1215
    category = "Advanced Artificial Intelligence Tools"
    class Outputs:
        data = Output("Data", Table, default=True)

    def __init__(self):
        self.opening_method = "image_file"
        self.info_label = gui.label(self.controlArea, self, "Initial info.")
        super().__init__()

    def process_files(self, files_to_process: list[Path]):
        images_files = [str(file_path) for file_path in files_to_process]
        table = self.create_image_table(images_files)
        self.Outputs.data.send(table)
    
    def create_image_table(self, image_files: List[str]) -> Table:
        # Define the metadata attributes for the images
        imagename_var = StringVariable.make("image name")
        imagepath_var = StringVariable.make("image path")
        imagepath_var.attributes["type"] = "image"  # Indicating type for Orange
        size_var = ContinuousVariable.make("size")
        width_var = ContinuousVariable.make("width")
        height_var = ContinuousVariable.make("height")

        domain = Domain(attributes=[], metas=[imagename_var, imagepath_var, size_var, width_var, height_var])

        meta_data = []
        
        for file_path in image_files:
            image_data = self.get_image_metadata(file_path)
            if image_data:
                meta_data.append(image_data)
        
        meta_data_array = np.array(meta_data, dtype=object)
        return Table.from_numpy(domain, X=np.empty((len(meta_data_array), 0)), metas=meta_data_array)

    def get_image_metadata(self, file_path: str):
        reader = QImageReader(file_path)
        if not reader.canRead():
            print(f"Cannot read image: {file_path}")
            return None

        img_format = bytes(reader.format()).decode("ascii")
        size = reader.size()
        width, height = (size.width(), size.height()) if size.isValid() else (float("nan"), float("nan"))
        try:
            st_size = os.stat(file_path).st_size
        except OSError:
            st_size = -1

        basename = os.path.basename(file_path)
        imgname, _ = os.path.splitext(basename)
        path_normalized = file_path.replace(os.path.sep, "/")

        return [imgname, path_normalized, st_size, width, height]

if __name__ == "__main__":
    from orangewidget.utils.widgetpreview import WidgetPreview
    WidgetPreview(OWLocalInterfaceImages).run()
