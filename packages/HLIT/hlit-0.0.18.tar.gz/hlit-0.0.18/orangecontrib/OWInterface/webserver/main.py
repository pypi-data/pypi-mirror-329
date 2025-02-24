from typing import List, Literal, Union

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse, HTMLResponse

from functions.workflow_management import launch_workflow, stop_workflow, get_workflow_status 
from functions.file_upload import upload_files, upload_files_via_path
from functions.lifespan_manager import lifespan
from functions.output_retrieval import retrieve_outputs
from functions.fileDialog import choose_file_on_server, choose_folder_on_server
from settings import TIMEOUT_LIMIT, SERVER_DESCRIPTION, SERVER_NAME, html_examples_directory
from fastapi.staticfiles import StaticFiles
from pathlib import Path

app = FastAPI(
    title = SERVER_NAME,
    description = SERVER_DESCRIPTION,
    lifespan=lifespan)

app.mount("/html_examples", StaticFiles(directory=str(html_examples_directory), html=True), name="html_examples")


# CORS Settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # List of origins that are allowed, '*' means allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # List of HTTP methods that are allowed, '*' means allow all methods
    allow_headers=["*"],  # List of headers that are allowed, '*' means allow all headers
    expose_headers=["Content-Disposition"]

)



# Main API Endpoints
@app.post("/upload-files/")
async def _upload_files(
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
    Upload multiple files to the server for processing through a Orange workflow. 
      
    Args:   
        - file_ids (List[str]): List of unique file IDs corresponding to the files.
          The IDs should match the ones configured in the Orange workflow.   
        - workflow_id (str): Unique ID of the workflow.
          The ID should match the one configured in the Orange workflow.   
        - opening_methods (List[str]): List of opening methods for the files.
          Choose from 'image_file', 'multiple_file', or 'file'.    
        - expected_nb_outputs (int): Expected number of output files (depending on your workflow).
        - files (List[UploadFile]): List of files to be uploaded.
        - text_inputs_id (List[str]): List of unique text input IDs corresponding to the text inputs.
            The IDs should match the ones configured in the Orange workflow.
        - text_inputs_value (List[str]): List of text input values corresponding to the text inputs.
        - timeout_limit (int): Timeout limit for the processing task (in seconds).

    Returns:   
        JSONResponse: Response message with the unique ID of the processing task."""

    return await upload_files(file_ids, workflow_id, opening_methods, expected_nb_outputs, files, text_inputs_id, text_inputs_value, timeout_limit)

@app.post("/upload-files-via-path/")
async def _upload_files_via_path(
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
    Upload multiple files to the server for processing through a Orange workflow.

    Args:   
        - filepaths (List[str]): List of file paths to be uploaded.   
        - file_ids (List[str]): List of unique file IDs corresponding to the files.
          The IDs should match the ones configured in the Orange workflow.  
        - opening_methods (List[str]): List of opening methods for the files.
          Choose from 'image_file', 'multiple_file', or 'file'.   
        - workflow_id (str): Unique ID of the workflow.
          The ID should match the one configured in the Orange workflow.   
        - expected_nb_outputs (int): Expected number of output files (depending on your workflow).
        - text_inputs_id (List[str]): List of unique text input IDs corresponding to the text inputs.
            The IDs should match the ones configured in the Orange workflow.
        - text_inputs_value (List[str]): List of text input values corresponding to the text inputs.
        - timeout_limit (int): Timeout limit for the processing task (in seconds).
    Returns:   
        JSONResponse: Response message with the unique ID of the processing task."""
    print("filepath received: ", filepaths)
    return await upload_files_via_path(filepaths, file_ids, opening_methods, workflow_id, expected_nb_outputs, text_inputs_id, text_inputs_value, timeout_limit)

@app.get("/retrieve-outputs/{unique_id}", response_model=None)
async def _retrieve_outputs(unique_id: str, 
                            file_id: str = "", 
                            return_mode: Literal["file", "json", "html"]="file",
                            delimiter = "\t") -> Union[FileResponse, JSONResponse, HTMLResponse]:
    """
    Retrieve the output files for a given unique ID. By default, a zip of all files will be returned.
    If a specific output filename is provided, only that file will be returned.   
    **IMPORTANT** : If the processing is not complete, the method will return a 404 error. You have to keep calling this method until the processing is complete.

    Args:     
        - unique_id (str): Unique ID of the processing task.  
        - file_id (str): Optional file ID to retrieve a specific file. If not provided, a zip of all files will be returned. 

    Returns:  
        FileResponse ou JSONResponse: Response with the output file(s) for download.
    """
    return await retrieve_outputs(unique_id, file_id, return_mode, delimiter)


@app.post("/launch-workflow/")
async def _launch_workflow(
    workflow_name: str,
    force_reload: bool = False,
    gui: bool = True
) -> JSONResponse:
    """
    Launch a workflow from an Orange file. The workflow will be executed in the background.

    Args:   
        - workflow (File): Orange workflow file to be executed.
    
    Returns:   
        JSONResponse: Response message, indicating that the workflow has been launched."""
    return await launch_workflow(workflow_name, force_reload, gui)
    
    
@app.post("/stop-workflow/")
async def _stop_workflow(
    workflow_id: str
) -> JSONResponse:
    """
    Stop a workflow that is currently running.

    Args:   
        - workflow_id (str): Unique ID of the workflow to be stopped.
    
    Returns:   
        JSONResponse: Response message, indicating that the workflow has been stopped."""
    return await stop_workflow(workflow_id)

@app.get("/get-running-workflows/")
async def _get_running_workflows() -> JSONResponse:
    """
    Get a list of all running workflows.

    Returns:   
        JSONResponse: Response message with the list of running workflows."""
    return await get_workflow_status()


@app.get("/choose-file-on-server/")
async def _choose_file_on_server() -> JSONResponse:
    """Open a file dialog to choose a file on the server."""
    return await choose_file_on_server()


@app.get("/select-folder/")
async def _select_folder() -> JSONResponse:
    """
    Opens a dialog window to let the user select a folder path.
    """
    return await choose_folder_on_server()


