from fastapi import FastAPI, Body
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.websockets import WebSocket, WebSocketDisconnect

from typing import Any
import websockets as wb
import uvicorn

import clr
from System import Object, Func             # type: ignore
from System.Windows import Application      # type: ignore

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def invoke_in_ui_thread(func: Any) -> Any:
    """ Executes provided function on UI thread.

    Args:
        func: Function to execute

    Returns:
        The same object that func returns
    """

    return Application.Current.Dispatcher.Invoke(Func[Object](func))



@app.get("/")
def health_check() -> dict:
    """Health Check function to check if server is running.

    Returns:
        dict: Dict representing the response.
    """
    return {"message": "Hello from a threaded FastAPI server with arguments!"}



@app.post("/create-elements")
def create_elements(payload: dict = Body(...)) -> JSONResponse:
    """ Endpoint to create elements using Grasshopper.

    Args:
        payload: A dictionary representing the elements.

    Returns:
        JSONResponse: Reponse object representing state.
    """
    _ = invoke_in_ui_thread(lambda: app.connection_handler.handle_create_elements(payload))
    return JSONResponse(content={"status": "200", "payload": None})


@app.websocket("/ws")
async def connet_websocket(websocket: WebSocket):
    """ Endpoint to handle websocket connections.

    Args:
        websocket: Websockt connection
    """
    await websocket.accept()
    try:
        print("Starting Websocket")
        while True:
            data = await websocket.receive_text()
            print(data)
            await websocket.send_text(f"Message text was: {data}")
    except WebSocketDisconnect:
        pass


# How to handler cord input
def init_app(connection_handler):
    """ Add connection handler to FastAPI server.

    Args:
        connection_handler: Connection hadnler which contains util functions to create elements.
    """
    app.connection_handler = connection_handler
    return app

def run_server(server: FastAPI):
    """ Function to run the fastAPI server.

    Args:
        server: FastAPI server instance.
    """
    config = uvicorn.Config(server, host="127.0.0.1", port=5679, log_level="info", ws_ping_interval=0, ws_max_size=16777216)
    server = uvicorn.Server(config)
    server.run()

def shutdown():
    """ShutDown Server Instance"""

    uvicorn.Server.should_exit = True
