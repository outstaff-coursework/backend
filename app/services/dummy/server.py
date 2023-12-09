from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
from uvicorn import run as uvicorn_run

app = FastAPI()


@app.get("/ping")
async def hello():
    return PlainTextResponse("OK")


def run_server():
    uvicorn_run(app, host="0.0.0.0", port=8000)
