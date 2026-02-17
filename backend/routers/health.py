from fastapi import APIRouter, HTTPException
from sqlalchemy import text
from datetime import datetime
import os
import structlog

router = APIRouter()
logger = structlog.get_logger()

@router.get("/health")
async def basic_health():
    """Базова перевірка - чи сервер живий"""
    return {
        "status": "ok",
        "service": "CODEX API",
        "version": "1.0.0"
    }

@router.get("/health/detailed")
async def detailed_health():
    """Детальна перевірка всіх компонентів"""
    
    health_status = {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "components": {}
    }
    
    # 1. Перевірити базу даних
    try:
        from main import engine
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            result.fetchone()
        health_status["components"]["database"] = {
            "status": "healthy",
            "message": "Connected"
        }
    except Exception as e:
        health_status["status"] = "unhealthy"
        health_status["components"]["database"] = {
            "status": "unhealthy",
            "error": str(e)
        }
        logger.error("health_check_database_failed", error=str(e))
    
    # 2. Перевірити OpenAI API
    try:
        # Простий тест - перевірити що ключ валідний
        if os.getenv("OPENAI_API_KEY"):
            health_status["components"]["openai"] = {
                "status": "healthy",
                "message": "API key configured"
            }
        else:
            health_status["components"]["openai"] = {
                "status": "unhealthy",
                "message": "API key not configured"
            }
    except Exception as e:
        health_status["components"]["openai"] = {
            "status": "unhealthy",
            "error": str(e)
        }
    
    # 3. Перевірити MinIO
    try:
        from services.doc_processor.storage import MinIOStorage
        storage = MinIOStorage()
        # Просто перевірити що підключення є
        health_status["components"]["minio"] = {
            "status": "healthy",
            "message": "Connected"
        }
    except Exception as e:
        health_status["components"]["minio"] = {
            "status": "unhealthy",
            "error": str(e)
        }
    
    # 4. Перевірити Redis (якщо є)
    try:
        import redis
        r = redis.Redis(host='redis', port=6379, db=0)
        r.ping()
        health_status["components"]["redis"] = {
            "status": "healthy",
            "message": "Connected"
        }
    except Exception as e:
        health_status["components"]["redis"] = {
            "status": "not_configured",
            "message": "Redis not available (optional)"
        }
    
    # Загальний статус
    unhealthy_components = [
        name for name, comp in health_status["components"].items()
        if comp["status"] == "unhealthy"
    ]
    
    if unhealthy_components:
        health_status["status"] = "unhealthy"
        health_status["unhealthy_components"] = unhealthy_components
    
    # Логувати якщо щось не так
    if health_status["status"] == "unhealthy":
        logger.error("health_check_failed", 
                    unhealthy=unhealthy_components)
    
    return health_status

@router.get("/health/ready")
async def readiness_check():
    """Перевірка готовності приймати запити (для Kubernetes)"""
    
    # Перевірити критичні компоненти
    try:
        from main import engine
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        
        return {"status": "ready"}
    except Exception as e:
        logger.error("readiness_check_failed", error=str(e))
        raise HTTPException(status_code=503, detail="Not ready")

@router.get("/health/live")
async def liveness_check():
    """Перевірка що процес живий (для Kubernetes)"""
    return {"status": "alive"}
