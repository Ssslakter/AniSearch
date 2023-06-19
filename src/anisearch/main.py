from fastapi import FastAPI
from src.anisearch.startup import services, config
from src.anisearch.endpoints import routers

app = FastAPI()
app.include_router(routers.router)


@app.on_event("startup")
async def startup_event():
    services.storage.init_collection(config.qdrant.collection_name)
    print("Server starting...")
