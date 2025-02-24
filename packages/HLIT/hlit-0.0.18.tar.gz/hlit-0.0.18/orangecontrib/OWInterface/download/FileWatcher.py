from pathlib import Path
from AnyQt.QtCore import QObject, pyqtSignal, QFileSystemWatcher

class FileWatcher(QObject):
    file_modified = pyqtSignal(str)

    def __init__(self, file_path: str):
        super(FileWatcher, self).__init__()
        self.watcher = QFileSystemWatcher()
        if not Path(file_path).exists():
            Path(file_path).parent.mkdir(parents=True, exist_ok=True)
            Path(file_path).touch()
        self.watcher.addPath(file_path)
        self.watcher.fileChanged.connect(self.on_file_modified)

    def on_file_modified(self, file_path):
        self.file_modified.emit(file_path)
