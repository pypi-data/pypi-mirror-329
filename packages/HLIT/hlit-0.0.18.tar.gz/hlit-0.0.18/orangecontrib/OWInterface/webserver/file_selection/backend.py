# backend.py
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
import os
from typing import List

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIRECTORY = r"C:\Users\33642\Documents"

def list_directory_contents(path: str):
    try:
        full_path = os.path.join(BASE_DIRECTORY, path)
        if not os.path.exists(full_path) or not os.path.isdir(full_path):
            raise FileNotFoundError(f"No such directory: {full_path}")

        items = []
        for entry in os.scandir(full_path):
            items.append({
                "name": entry.name,
                "is_folder": entry.is_dir()
            })
        return items
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.get("/list-directory")
async def list_directory(sub_path: str = Query("")):
    # List contents of the directory at the given sub_path
    return list_directory_contents(sub_path)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
