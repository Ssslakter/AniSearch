from pathlib import Path
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from src.anisearch.startup import start_up
from src.anisearch.endpoints import api

curr_dir = Path(__file__).parent
app = FastAPI()
app.include_router(api.router)
app.mount("/static", StaticFiles(directory=str(curr_dir / "static")))


@app.get("/", response_class=FileResponse)
async def get_index():
    return FileResponse(str(curr_dir / "static" / "index.html"))


@app.on_event("startup")
async def startup_event():
    start_up()
