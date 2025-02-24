from typing import List, Dict, Any, Tuple
from fastapi import File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from settings import TIMEOUT_LIMIT, save_directory, output_directory, waiting_queue
from functions.utils import make_list, generate_unique_output_folder
from pathlib import Path

async def upload_files(
    file_ids: List[str], 
    workflow_id: str,
    opening_methods: List[str], 
    expected_nb_outputs: int, 
    files: List[UploadFile] = File(default=None),
    text_inputs_id: List[str] = [],
    text_inputs_value: List[str] = [],
    timeout_limit: int = TIMEOUT_LIMIT,    
) -> JSONResponse:
    """
    Upload multiple files to the server for processing through an Orange workflow.

    Args:   
        - file_ids (List[str]): List of unique file IDs corresponding to the files.
        - workflow_id (str): Unique ID of the workflow.
        - opening_methods (List[str]): List of opening methods for the files.
        - expected_nb_outputs (int): Expected number of output files.
        - files (List[UploadFile]): List of files to be uploaded.
        - text_inputs_id (List[str]): List of text input IDs for the workflow.
        - text_inputs_value (List[str]): List of text input values for the workflow.
        - timeout_limit (int): Timeout limit for the processing task.


    Returns:
        JSONResponse: Response message with the unique ID of the processing task.
    """

    # Save files to disk and collect filepaths
    filepaths = []
    if files is None:
        files = []
    for file in files:
        content: bytes = await file.read()
        input_filename: str = str(save_directory / str(file.filename))
        
        # Save the file locally
        with open(input_filename, 'wb') as f:
            f.write(content)

        filepaths.append(input_filename)

    # Delegate processing to upload_files_via_path using stored filepaths
    return await upload_files_via_path(
        filepaths=filepaths,
        file_ids=file_ids,
        opening_methods=opening_methods,
        workflow_id=workflow_id,
        expected_nb_outputs=expected_nb_outputs,
        timeout_limit=timeout_limit,
        text_inputs_id=text_inputs_id,
        text_inputs_value=text_inputs_value
    )

async def upload_files_via_path(
    filepaths: List[str],
    file_ids: List[str],
    opening_methods: List[str],
    workflow_id: str, 
    expected_nb_outputs: int,
    text_inputs_id: List[str] = [],
    text_inputs_value: List[str] = [],
    timeout_limit: int = TIMEOUT_LIMIT,

) -> JSONResponse:
    """
    Process files obtained via file paths for an Orange workflow.

    Args:   
        - filepaths (List[str]): List of file paths to be processed.
        - file_ids (List[str]): List of unique file IDs corresponding to the files.
        - opening_methods (List[str]): List of opening methods for the files.
        - workflow_id (str): Unique ID of the workflow.
        - expected_nb_outputs (int): Expected number of output files.
        - text_inputs_id (List[str]): List of text input IDs for the workflow.
        - text_inputs_value (List[str]): List of text input values for the workflow.
        - timeout_limit (int): Timeout limit for the processing task.

    Returns:   
        JSONResponse: Response message with the unique ID of the processing task.
    """

    # Convert inputs to lists to maintain uniformity
    file_ids = make_list(file_ids)
    opening_methods = make_list(opening_methods)
    filepaths = make_list(filepaths)
    text_inputs_id = make_list(text_inputs_id)
    text_inputs_value = make_list(text_inputs_value)

    # Validate input lengths
    if len(filepaths) != len(file_ids) or len(file_ids) != len(opening_methods):
        print("filepaths: ", filepaths)
        print("file_ids: ", file_ids)
        print("opening_methods: ", opening_methods)
        raise HTTPException(status_code=400, detail="Numbers of file paths, file IDs, and opening methods must match.")

    if expected_nb_outputs <= 0:
        raise HTTPException(status_code=400, detail="Expected number of outputs must be at least 1.")

    file_entries: List[Dict[str, Any]] = []
    for filepath, file_id, opening_method in zip(filepaths, file_ids, opening_methods):
        if opening_method not in ["image_file", "multiple_file", "file"]:
            raise HTTPException(status_code=400, detail="Invalid opening method provided.")
        
        file_path: Path = Path(filepath)
        if not file_path.exists():
            raise HTTPException(status_code=404, detail=f"File not found: {filepath}")

        file_entries.append({
            'input_filename': str(file_path),
            'file_id': file_id,
            'opening_method': opening_method
        })

    unique_id, output_folder = generate_unique_output_folder(output_directory)

    waiting_queue.add({
        'unique_id': unique_id,
        'workflow_id': workflow_id,
        'file_entries': file_entries,
        'output_folder': str(output_folder),
        'expected_nb_outputs': expected_nb_outputs,
        'text_inputs_id': text_inputs_id,
        'text_inputs_value': text_inputs_value,
        'timeout_limit': timeout_limit
    })

    return JSONResponse(content={"message": "Files queued for processing", "unique_id": unique_id})
