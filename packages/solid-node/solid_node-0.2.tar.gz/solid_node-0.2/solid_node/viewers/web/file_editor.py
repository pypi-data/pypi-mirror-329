import os
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse, FileResponse, RedirectResponse
import logging

logger = logging.getLogger(__name__)

def filesystem_app(basedir):
    app = FastAPI()

    @app.get("/{url_path:path}")
    async def serve_path(request: Request, path: str):
        import ipdb; ipdb.set_trace()
        while path.startswith('/'):
            path = path[1:]
        if '..' in path:
            return
        full_path = os.path.join(basedir, path)

        if os.path.isdir(full_path):
            if not path.endswith("/"):
                # Redirect folder paths that do not end with /
                return RedirectResponse(url=request.url.path + "/")
            return JSONResponse(content=build_tree(full_path, path))

        elif os.path.isfile(full_path):
            if path.endswith("/"):
                # Raise 404 for files requested with a trailing slash
                raise HTTPException(status_code=404, detail="File not found")
            return FileResponse(full_path)
        else:
            raise HTTPException(status_code=404, detail="Path not found")

    def build_tree(full_path, path):
        import ipdb; ipdb.set_trace()
        tree = {
            "name": os.path.basename(path),
            "path": path,
            "isFile": os.path.isfile(full_path),
        }
        if os.path.isdir(full_path):
            tree["children"] = []
            for item in sorted(os.listdir(full_path)):
                item_path = os.path.join(full_path, item)
                item_relative_path = os.path.join(path, item)
                tree["children"].append(build_tree(item_path, item_relative_path))
        return tree

    return app
