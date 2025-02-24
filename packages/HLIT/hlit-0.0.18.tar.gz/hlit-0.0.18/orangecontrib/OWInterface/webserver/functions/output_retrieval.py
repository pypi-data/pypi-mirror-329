from settings import output_directory, FINAL_FOLDER_ARCHIVE_NAME, FINAL_FILE_NAME
from fastapi.responses import FileResponse, JSONResponse, HTMLResponse
from pathlib import Path
from functions.utils import zip_folder
from typing import Literal, Union, List, Dict
import csv

def csv_to_json_compatible(csv_path: str, delimiter: str) -> Dict[str, List[str]]:
    """
    Convert CSV data to a JSON-compatible dictionary structure, ensuring all columns have the same size.

    Args:
        csv_path (str): Path to the CSV file.

    Returns:
        Dict[str, List[str]]: A JSON-compatible dictionary representation of the CSV.

    Raises:
        ValueError: If columns have differing lengths.
    """
    with open(csv_path, mode='r', newline='', encoding="utf-8") as f:
        # Read the first 10 lines to infer the delimiter
        sample_lines = ''.join([f.readline() for _ in range(10)])
        

        f.seek(0)  # Reset file read pointer

        reader = csv.reader(f, delimiter=delimiter)
        headers = next(reader)
        
        # Initialize dictionary with headers
        data = {header: [] for header in headers}

        _ = next(reader)  # Skip the second line. Contains the data type information.
        line = next(reader) 
        if line[0] == "meta" or all(line.strip() == "" for line in line):
            pass # Skip the metadata line
        else:
            print("delimiter: ", delimiter)
            raise ValueError(f"""Second line of CSV file should contain metadata information. This function needs
                              to be updated to handle this case. Ensure that you set the correct delimiter in your function.
                             line: {line},
                             line[0]: {line[0]},
                             line_type: {type(line)},
                             line[0]_type: {type(line[0])}""")


        for row in reader:
            for header, value in zip(headers, row):
                data[header].append(value.strip())
        
        # Check column lengths
        column_lengths = [len(column) for column in data.values()]
        if len(set(column_lengths)) != 1:
            raise ValueError("CSV columns have inconsistent lengths.")

    return data

def csv_to_html_table(csv_path: str, delimiter: str) -> str:
    """
    Convert CSV data to an HTML table format string using the validated JSON-compatible data.

    Args:
        csv_path (str): Path to the CSV file.

    Returns:
        str: A string representation of the HTML table.
    """
    data = csv_to_json_compatible(csv_path, delimiter)

    # Create HTML table header
    headers = data.keys()
    html = "<table border='1'><thead><tr>"
    for header in headers:
        html += f"  <th>{header}</th>"
    html += "</tr></thead><tbody>"

    # Get number of rows (validated as consistent in csv_to_json_compatible)
    num_rows = len(next(iter(data.values())))

    # Fill table rows
    for i in range(num_rows):
        html += "<tr>"
        for header in headers:
            value = data[header][i]
            html += f"  <td>{value}</td>"
        html += "</tr>"
    html += "</tbody></table>"

    return html

async def is_processing_complete(output_folder: Path) -> bool:
    """
    Determine if processing is complete based on the existence of a 'done' file.
    
    Args:
        output_folder (Path): Path to the output directory for a specific task.
    
    Returns:
        bool: True if processing is complete, False otherwise.
    """
    return (output_folder / FINAL_FILE_NAME).exists()

async def get_all_files(output_folder: Path) -> List[Path]:
    """
    Retrieve all relevant files from an output directory, excluding metadata files.
    
    Args:
        output_folder (Path): Path to the output directory for a specific task.
    
    Returns:
        List[Path]: List of file paths in the directory.
    """
    all_files = list(output_folder.glob('*'))
    
    for file in [output_folder / FINAL_FILE_NAME, output_folder / FINAL_FOLDER_ARCHIVE_NAME]:
        if file.exists():
            all_files.remove(file)
    
    return all_files

async def retrieve_outputs(unique_id: str, file_id: str, return_mode: Literal["file", "json", "html"], delimiter:str) -> Union[FileResponse, JSONResponse, HTMLResponse]:
    """
    Retrieve outputs as either file or JSON based on the specified return mode.
    
    Args:
        unique_id (str): Unique identifier for the processing task.
        file_id (str): Optional identifier for a specific file to retrieve.
        return_mode (Literal["file", "json"]): The desired return format.
    
    Returns:
        Union[FileResponse, JSONResponse]: Response with the requested output.
    """
    output_folder = output_directory / unique_id
    
    if not await is_processing_complete(output_folder):
        if output_folder.exists():
            return JSONResponse(content={"message": "Processing is not complete."}, status_code=404)
        else:
            return JSONResponse(content={"message": "Unique ID not found."}, status_code=404)
    
    all_files = await get_all_files(output_folder)

    if return_mode == "file":
        return await retrieve_outputs_as_file(all_files, file_id, output_folder)
    
    elif return_mode == "json":
        return await retrieve_outputs_as_json(all_files, delimiter)
    elif return_mode == "html":
        return retrieve_outputs_as_html(all_files, delimiter)
    

async def retrieve_outputs_as_file(all_files: List[Path], file_id: str, output_folder: Path) -> Union[FileResponse, JSONResponse]:
    """
    Return files as either a specific file or a zip archive of all files.
    
    Args:
        all_files (List[Path]): List of available files in the output directory.
        file_id (str): Identifier for a specific file to retrieve.
        output_folder (Path): Path to the output folder.
    
    Returns:
        Union[FileResponse, JSONResponse]: Response with the requested file(s).
    """

    if file_id:
        for file in all_files:
            if file_id in file.name:
                return FileResponse(str(file), media_type='application/octet-stream', filename=file.name)
        return JSONResponse(content={"message": f"File with ID {file_id} not found."}, status_code=404)

    if len(all_files) == 1:
        output_file = all_files[0]
        return FileResponse(str(output_file), media_type='application/octet-stream', filename=output_file.name)
    elif len(all_files) > 1:
        output_zip: Path = output_folder / FINAL_FOLDER_ARCHIVE_NAME
        zip_folder(output_folder, output_zip)
        return FileResponse(str(output_zip), media_type='application/zip', filename=FINAL_FOLDER_ARCHIVE_NAME)
    else:
        return JSONResponse(content={"message": "No files found in the output folder."}, status_code=404)

async def retrieve_outputs_as_json(all_files: List[Path], delimiter: str) -> JSONResponse:
    """
    Return JSON response after converting available CSV files to JSON-compatible structures.
    
    Args:
        all_files (List[Path]): List of available files in the output directory.
    
    Returns:
        JSONResponse: Response with JSON data of all CSV files.
    """
    results = []
    for file in all_files:
        if file.suffix == '.csv':
            json_data = csv_to_json_compatible(str(file), delimiter)
            results.append({
                "filename": file.name,
                "content": json_data
            })
        else:
            raise ValueError(f"File {file.name} is not a CSV file. This is unexpected.")

    if not results:
        return JSONResponse(content={"message": "No CSV files found for conversion."}, status_code=404)

    return JSONResponse(content=results)


def retrieve_outputs_as_html(all_files: List[Path], delimiter: str) -> HTMLResponse:
    """
    Return HTML response after converting available CSV files to HTML tables.

    Args:
        all_files (List[Path]): List of available files in the output directory.

    Returns:
        HTMLResponse: Response with HTML content of all CSV files.
    """
    html_content = ""
    
    for file in all_files:
        if file.suffix == '.csv':
            html_table = csv_to_html_table(str(file), delimiter=delimiter)
            html_content += f"<h2>{file.name}</h2>{html_table}<br>"
        else:
            raise ValueError(f"File {file.name} is not a CSV file. This is unexpected.")

    if html_content == "":
        return HTMLResponse("No CSV files found for conversion.", status_code=404)

    return HTMLResponse(content=html_content)
