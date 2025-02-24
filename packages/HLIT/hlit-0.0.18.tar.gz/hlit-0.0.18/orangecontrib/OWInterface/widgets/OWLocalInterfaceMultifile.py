import json
import os
from itertools import chain, repeat
from pathlib import Path
from pprint import pprint
from typing import Union

import numpy as np
from AnyQt.QtCore import QFileSystemWatcher, QObject, pyqtSignal
from Orange.data import Domain, StringVariable, Table
from Orange.widgets import gui, settings, widget

if "site-packages/Orange/widgets" in os.path.dirname(os.path.abspath(__file__)).replace("\\", "/"):
    from Orange.widgets.orangecontrib.AAIT.download.BaseLocalInterfaceWidget import BaseLocalInterfaceWidget
    from Orange.widgets.orangecontrib.AAIT.webserver.start_server import start_server
else:
    from orangecontrib.OWInterface.download.BaseLocalInterfaceWidget import BaseLocalInterfaceWidget
    from orangecontrib.OWInterface.webserver.start_server import start_server


class OWLocalInterfaceMultifile(BaseLocalInterfaceWidget): # type: ignore
    name = "Local Interface - Multifile"
    description = "Get multiple data file (csv, xlsx, pkl...) from a local interface"
    icon = "icons/local_interf_multi_pull.svg"
    if "site-packages/Orange/widgets" in os.path.dirname(os.path.abspath(__file__)).replace("\\", "/"):
        icon = "icons_dev/local_interf_multi_pull.svg"
    priority = 1213
    category = "Advanced Artificial Intelligence Tools"
    class Outputs:
        data = widget.Output("Data", Table)

    def __init__(self):
        self.opening_method = "multiple_file"
        super().__init__()

    def process_files(self, files_to_process: list[Path]):
        data = self.concatenate_data_with_origin(files_to_process)
        self.Outputs.data.send(data)

    def concatenate_data_with_origin(self, filepaths: list[Path])->Union[Table,None]:
        if not filepaths:
            return None
        
        filenames = [filepath.name for filepath in filepaths]
        tables = [Table.from_file(str(x)) for x in filepaths]

        # Determine the merged domain, accounting for all attributes and metas in all tables
        domain = self._merge_domains([table.domain for table in tables])
        source_var = StringVariable("File Source")
        domain = Domain(domain.attributes, domain.class_vars, domain.metas + (source_var,))

        # Transform tables to the new domain so they can be concatenated
        tables = [table.transform(domain) for table in tables]
        data = Table.concatenate(tables)

        with data.unlocked():
            # Flatten the array to the correct shape
            data.metas[:, -1] = np.array(list(
                chain(*(repeat(fn, len(table))
                        for fn, table in zip(filenames, tables)))
            ))

        return data

    def _merge_domains(self, domains):
        # This assumes all tables have compatible domains; more complex logic can be implemented if needed
        return domains[0] if domains else Domain([])

if __name__ == "__main__":
    # This would normally start the GUI application
    pass
