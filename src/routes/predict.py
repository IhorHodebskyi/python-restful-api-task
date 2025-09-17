from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
from src.ml.ml_service import predictor
from src.celery_app import train_ml_model

router = APIRouter(prefix="/predict", tags=["predict"])


class PredictionRequest(BaseModel):
    task_description: str


class PredictionResponse(BaseModel):
    priority: str
    confidence: float
    task_description: str


@router.post("/", response_model=PredictionResponse)
async def predict_priority(request: PredictionRequest):
    try:
        result = predictor.predict_priority(request.task_description)

        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])

        return PredictionResponse(**result)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")


@router.post("/train")
async def train_model():
    try:
        task = train_ml_model.delay()
        return {
            "message": "Model training started in background",
            "task_id": task.id
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Training error: {str(e)}")


@router.get("/task-status/{task_id}")
async def get_task_status(task_id: str):
    try:
        from src.celery_app import celery_app
        result = celery_app.AsyncResult(task_id)
        return {
            "task_id": task_id,
            "status": result.status,
            "result": result.result if result.ready() else None
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error checking task status: {str(e)}")


@router.get("/healthchecker")
async def ml_health_check():
    try:
        if predictor.model is not None:
            return {"status": "ready", "message": "Model is loaded"}
        elif predictor.load_model():
            return {"status": "ready", "message": "Model loaded from file"}
        else:
            return {"status": "not_trained", "message": "Model needs training"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Health check failed: {str(e)}")
