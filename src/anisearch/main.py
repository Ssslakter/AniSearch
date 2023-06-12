from fastapi import FastAPI
from src.anisearch.startup import services, config
from src.anisearch.endpoints import admin

app = FastAPI()
app.include_router(admin.router)


@app.on_event("startup")
async def startup_event():
    services.storage.init_collection(config.qdrant.collection_name)
    print("Server starting...")
