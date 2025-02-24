import os
from fastapi import FastAPI, Request, Response, HTTPException
from fastapi.responses import FileResponse

class FilesystemAPI:

    def __init__(self, path):
        self.basedir = os.path.realpath(
            os.path.dirname(path)
        )

        self.app = FastAPI()
        self.app.add_api_route('/{file_path:path}', self.serve_path)

    async def serve_path(self, file_path: str):
        full_path = os.path.join(self.basedir, file_path)
        if not os.path.realpath(full_path).startswith(self.basedir):
            raise HTTPException(status_code=403, detail="Access denied")

        if os.path.isdir(full_path):
            return self.list_directory(full_path)
        elif os.path.isfile(full_path):
            return FileResponse(full_path)
        else:
            raise HTTPException(status_code=404, detail="File or directory not found")

    def list_directory(self, path: str):
        try:
            entries = os.listdir(path)
            return {"contents": entries}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
