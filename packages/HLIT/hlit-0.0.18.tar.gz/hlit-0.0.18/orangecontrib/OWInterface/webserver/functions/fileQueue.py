import json
from pathlib import Path
from typing import Any, Dict, List


class FileQueue:
    """
    A queue that persists its state to a file.
    Ensure that the memory state of the queue is always in sync with the file state.
    Also, ensure that each item in the queue is unique.
    """
    def __init__(self, file_path: Path):
        self.file_path: Path = file_path # path to json file to be processed
        self.queue: List[Dict[str, Any]] = []
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        self.file_path.touch(exist_ok=True)

        # Ensure to reset the queue to empty list, in case file wasn't empty
        self.save_queue()

    def load_queue(self) -> List[Dict[str, Any]]:
        """Load queue from the file, or initialize an empty queue if the file does not exist."""
        if self.file_path.exists():
            with open(self.file_path, 'r') as file:
                return json.load(file)
        else:
            return []

    def save_queue(self) -> None:
        """Persist the current state of the queue to a file."""
        with open(self.file_path, 'w') as file:
            json.dump(self.queue, file)


    def add(self, item: Dict[str, Any]) -> None:
        """Add an item to the queue and save the updated queue."""
        if item not in self.queue:
            self.queue.append(item)
            self.save_queue()
        else:
            print(f"Attempted to add duplicate item to queue. Add operation was ignored.")

    def remove(self, item: Dict[str, Any]) -> None:
        """Remove an item from the queue and save the updated queue."""
        if item in self.queue:
            self.queue.remove(item)
            self.save_queue()
        else:
            print(f"Attempted to remove non-existent item from queue: {item}")