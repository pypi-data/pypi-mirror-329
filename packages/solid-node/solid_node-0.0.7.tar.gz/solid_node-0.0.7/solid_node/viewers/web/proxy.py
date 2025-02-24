import httpx
import asyncio
import uvicorn
from fastapi import FastAPI, Request, WebSocket, Response

class ProxyServer:
    def __init__(self, port: int = 8000, target_port = 8001):
        self.app = FastAPI()
        self.target_url = f'http://localhost:{target_port}'
        self.host = '127.0.0.1'
        self.port = port

        @self.app.api_route("/{full_path:path}", methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"])
        async def proxy_request(full_path: str, request: Request):
            async with httpx.AsyncClient() as client:
                resp = await client.request(
                    method=request.method,
                    url=f"{self.target_url}/{full_path}",
                    headers=request.headers.raw,
                    data=await request.body(),
                    allow_redirects=False
                )
                return Response(content=resp.content, status_code=resp.status_code, headers=dict(resp.headers))

        @self.app.websocket("/ws/reload")
        async def websocket_endpoint(websocket: WebSocket):
            await websocket.accept()
            waiting = False
            while True:
                try:
                    async with httpx.AsyncClient() as client:
                        await client.get(self.target_url)
                        await websocket.send_text("available")
                        waiting = False
                except httpx.RequestError:
                    if not waiting:
                        await websocket.send_text("wait")
                        waiting = True
                await asyncio.sleep(0.1)

    def start(self):
        uvicorn.run(self.app, host='127.0.0.1', port=self.port)
