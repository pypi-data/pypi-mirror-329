

import hashlib
import uuid
import zipfile
from pathlib import Path
from typing import Tuple, List
from settings import FINAL_FOLDER_ARCHIVE_NAME, FINAL_FILE_NAME
import ast

def hash_file_content(content: bytes) -> str:
    """Compute the MD5 hash of a given content."""
    return hashlib.md5(content).hexdigest()

def generate_unique_output_folder(output_directory: Path) -> Tuple[str, Path]:
    """Generate a directory for the outputs using a UUID."""
    unique_id: str = str(uuid.uuid4())
    output_folder: Path = output_directory / unique_id
    output_folder.mkdir(exist_ok=True)
    return unique_id, output_folder

def make_list(liste: list) -> list:
    """Convert a string with comma-separated values to a list."""
    if len(liste) == 1:
        if liste[0][0]== "[" and liste[0][-1] == "]":
            return ast.literal_eval(liste[0])
        
        elif "," in liste[0]:
            return liste[0].split(",")
        else:
            return liste
    else:
        return liste
    
def zip_folder(
          source_dir: Path, 
          output_filename: Path, 
          excluded_files: list[str]=[FINAL_FILE_NAME, FINAL_FOLDER_ARCHIVE_NAME]
          ):
    """Zip the contents of a folder, excluding certain files."""
    if output_filename.exists():
        print("Output file already exists. Skipping zipping.")
        return
    with zipfile.ZipFile(output_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
         for file_path in source_dir.rglob('*'):
                    if file_path.is_file() and file_path.name not in excluded_files:
                        # Write the file to the archive with an appropriate relative path
                        zipf.write(file_path, file_path.relative_to(source_dir))





def clean_directory(directory: Path) -> None:
    """Remove all files in the workflow directory."""
    for file in directory.iterdir():
        try:
            file.unlink(missing_ok=True)
        except:
            pass
    

def make_tuple_list(text_inputs: List[str]) -> List[tuple[str, str]]:
    assert len(text_inputs) % 2 == 0, "The number of text inputs must be even."
    print("text_inputs: ", text_inputs)
    return [(text_inputs[i], text_inputs[i+1]) for i in range(0, len(text_inputs), 2)]

def ping():
    return "Pong"