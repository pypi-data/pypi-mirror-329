from fastapi import HTTPException
from fastapi.responses import JSONResponse
from pathlib import Path
import subprocess
import sys
from settings import workflow_directory
import os
import asyncio

processes: dict[Path, subprocess.Popen] = {}
def start_workflow(workflow_path: Path, gui: bool) -> None:
    """Launch a workflow using the command line and store the process information."""
    # 1. Delete .ows.swp files. These are temporary files created by vim when editing the .ows file.
    # By deleting, we avoid the PopUp Message "Restore unsaved changes from crash" when opening the workflow.
    for file in workflow_directory.glob("*.ows.swp.*"):
        file.unlink()

    # 2. Construct the command to run the workflow
    python_path = Path(sys.executable)
    command = [str(python_path), "-m", "Orange.canvas", str(workflow_path)]

    # 3. Prepare the environment for the subprocess
    env = dict(os.environ)  # Start with a copy of the current environment
    if not gui:
        env['QT_QPA_PLATFORM'] = 'offscreen'

    # Use subprocess.Popen to gain access to the process details
    process = subprocess.Popen(command, env=env)
    processes[workflow_path] = process

def kill_workflow(workflow_path: Path) -> None:
    """Stop a workflow by killing the process."""
    process = processes.get(workflow_path)
    if process:
        process.kill()
        del processes[workflow_path]
    else:
        print("No process to stop. Really weird.")

async def launch_workflow(
    workflow_name: str,
    force_reload: bool,
    gui: bool
) -> JSONResponse:
    """
    Launch a workflow from an Orange file. The workflow will be executed in the background.

    Args:   
        - workflow (File): Orange workflow file to be executed.
    
    Returns:   
        JSONResponse: Response message, indicating that the workflow has been launched."""
    
    workflow_path = workflow_directory / workflow_name
    if not workflow_path.exists():
        print(f"Workflow not found: {workflow_path}")
        raise HTTPException(status_code=404, detail="Workflow not found.")

    if not force_reload and (workflow_path in processes):
        # check if the workflow is done.
        if processes[workflow_path].poll() is None:
            print("processes[workflow_path].poll(): ", processes[workflow_path].poll())
            return JSONResponse(content={"message": "Workflow already started. Skipping."})
        else:
            start_workflow(workflow_path, gui)
            return JSONResponse(content={"message": "Workflow launched."})
    elif force_reload and (workflow_path in processes):
        kill_workflow(workflow_path)
        start_workflow(workflow_path, gui)
        print("processes: ", processes.keys())
        return JSONResponse(content={"message": "Workflow reloaded."})
    else:
        start_workflow(workflow_path, gui)
        print("processes: ", processes.keys())
        return JSONResponse(content={"message": "Workflow launched."})
    

async def stop_workflow(
    workflow_id: str
) -> JSONResponse:
    """
    Stop a workflow that is currently running.

    Args:   
        - workflow_id (str): Unique ID of the workflow to be stopped.
    
    Returns:   
        JSONResponse: Response message, indicating that the workflow has been stopped."""
    if workflow_id.endswith(".ows"):
        workflow_path: Path = workflow_directory / workflow_id
    else:
        workflow_path: Path = workflow_directory / (workflow_id + ".ows")
    if workflow_path.exists():
        kill_workflow(workflow_path)
        return JSONResponse(content={"message": "Workflow stopped.", "workflow_id": workflow_id})
    else:
        return JSONResponse(content={"message": "Workflow not found.", "workflow_id": workflow_id}, status_code=404)
    

async def get_workflow_status() -> JSONResponse:
    """
    Get a list of all running workflows.

    Returns:   
        JSONResponse: Response message with the list of running workflows."""
    
    # First step. Delete finished processes
    to_delete: list[Path]= []
    for k,v in processes.items():
        process = v
        if process.poll() is not None:
            to_delete.append(k)
    for k in to_delete:
        await stop_workflow(k.stem)

    # Second step. Return the running processes
    working_process = []
    for k,v in processes.items():
            working_process.append(k.name)

    available_workflows = [p.name for p in workflow_directory.glob("*.ows") if p not in working_process]
        
    return JSONResponse(content={"running_workflows": working_process, "available_workflows": available_workflows})

async def poll_processes_async(interval: float = 1.0):
    while True:
        to_delete: list[Path]= []
        for workflow_path, process in processes.items():
            if process.poll() is not None:
                to_delete.append(workflow_path)
        for workflow_path in to_delete:
            del processes[workflow_path]
        await asyncio.sleep(interval)

# Schedule this function to run in the event loop
asyncio.create_task(poll_processes_async())



## IMPORTANT ##
# Some errors is still possible if the user try to run a workflow from HTTP, just after closing it manually.
# This is because the process is still in the dictionary, but the workflow is not running anymore.
# Despite being unvisible, process takes ~1 second to be deleted by windows, after clicking on cross.
# Moreover, the processes dict is updated every second, meaning a latence up to 2 seconds, between visual closing
# and the process being deleted from the dictionary.

# This is a known issue, but no easy fix, so we'll leave it as it is for now.
# Theorically, probabilities of this happening are really low.
# If it happens, the user can just try to run the workflow again.