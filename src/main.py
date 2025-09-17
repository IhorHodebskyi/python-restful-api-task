from fastapi import FastAPI
from fastapi.exceptions import HTTPException
import logging

from src.routes.tasks import router as tasks_router
from src.routes.users import router as users_router
from src.routes.predict import router as predict_router
from src.database.storage import storage
from src.ml.ml_service import initialize_model


logger = logging.getLogger(__name__)

app = FastAPI()

app.include_router(prefix="/api", tags=["tasks"], router=tasks_router)
app.include_router(prefix="/api", tags=["users"], router=users_router)
app.include_router(prefix="/api", tags=["predict"], router=predict_router)


@app.on_event("startup")
async def startup_event():
    logger.info("Initializing ML model...")
    initialize_model()
    logger.info("ML model initialized")


@app.get("/api/healthchecker")
async def health_check():
    try:
        result = storage.get_tasks_count()
        if result is None:
            raise HTTPException(status_code=500, detail="Storage is not initialized")
        return {"status": "200", "message": "Service is running with in-memory storage"}
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(status_code=500, detail="Health check failed")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
