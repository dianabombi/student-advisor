"""
Celery Tasks for Document Processing

Асинхронні задачі для обробки документів та періодичного очищення.
"""

from celery import Task
from celery_app import celery_app
from datetime import datetime, timedelta
from celery.schedules import crontab
import traceback
import logging

logger = logging.getLogger(__name__)


@celery_app.task(bind=True, max_retries=3)
def process_document_task(self: Task, document_id: int):
    """
    Асинхронна обробка документа
    
    Args:
        document_id: ID документа для обробки
        
    Returns:
        Результат обробки
    """
    from database import SessionLocal
    from main import DocumentProcessingJob
    from services.doc_processor.processor import DocumentProcessor
    from services.doc_processor.storage import MinIOStorage
    
    db = SessionLocal()
    
    try:
        # Отримати задачу з БД
        job = db.query(DocumentProcessingJob).filter_by(document_id=document_id).first()
        if not job:
            logger.error(f"Job not found for document_id: {document_id}")
            return {"error": "Job not found"}
        
        # Оновити статус
        job.status = "processing"
        job.progress = 10
        db.commit()
        logger.info(f"Started processing document {document_id}")
        
        # Ініціалізувати процесор
        processor = DocumentProcessor()
        storage = MinIOStorage()
        
        # Завантажити файл з MinIO
        file_data = storage.download_file(job.raw_object_name)
        job.progress = 20
        db.commit()
        
        # Обробити документ
        result = processor.process_document(
            file_data=file_data,
            filename=job.filename,
            extract_fields=True,
            use_ai=True
        )
        
        # Оновити результати
        job.document_type = result['classification'].get('classification', 'unknown')
        job.confidence = result['classification'].get('confidence', 0.0)
        job.extracted_fields = result.get('extracted_fields', {})
        job.summary = result.get('summary', '')
        job.progress = 100
        job.status = "completed"
        job.processed_at = datetime.now()
        db.commit()
        
        logger.info(f"Successfully processed document {document_id}")
        
        return {
            "status": "success",
            "document_id": document_id,
            "document_type": job.document_type,
            "confidence": job.confidence
        }
        
    except Exception as e:
        # При помилці - зберегти інформацію
        logger.error(f"Error processing document {document_id}: {e}")
        logger.error(traceback.format_exc())
        
        job.status = "failed"
        job.error_message = str(e)
        job.progress = 0
        db.commit()
        
        # Спробувати ще раз (максимум 3 рази)
        try:
            raise self.retry(exc=e, countdown=60)  # Почекати 60 сек перед retry
        except self.MaxRetriesExceededError:
            logger.error(f"Max retries exceeded for document {document_id}")
            return {"error": str(e), "document_id": document_id}
        
    finally:
        db.close()


@celery_app.task
def cleanup_old_documents():
    """
    Видалити старі документи (запускається автоматично щодня о 3:00)
    
    Видаляє документи старші 90 днів
    """
    from database import SessionLocal
    from main import DocumentProcessingJob
    from services.doc_processor.storage import MinIOStorage
    
    db = SessionLocal()
    storage = MinIOStorage()
    
    try:
        cutoff_date = datetime.now() - timedelta(days=90)
        old_jobs = db.query(DocumentProcessingJob).filter(
            DocumentProcessingJob.processed_at < cutoff_date
        ).all()
        
        deleted_count = 0
        for job in old_jobs:
            try:
                # Видалити файли з MinIO
                if job.raw_object_name:
                    storage.delete_file(job.raw_object_name)
                if job.processed_object_name:
                    storage.delete_file(job.processed_object_name)
                
                # Видалити запис з БД
                db.delete(job)
                deleted_count += 1
            except Exception as e:
                logger.error(f"Error deleting job {job.document_id}: {e}")
        
        db.commit()
        logger.info(f"Cleanup completed: deleted {deleted_count} old documents")
        
        return {"deleted": deleted_count, "cutoff_date": cutoff_date.isoformat()}
        
    except Exception as e:
        logger.error(f"Error in cleanup task: {e}")
        db.rollback()
        return {"error": str(e)}
        
    finally:
        db.close()


@celery_app.task
def generate_embeddings_batch(document_ids: list):
    """
    Генерувати embeddings для багатьох документів паралельно
    
    Args:
        document_ids: Список ID документів
    """
    from database import SessionLocal
    from main import DocumentProcessingJob
    from services.rag.embeddings import EmbeddingService
    
    db = SessionLocal()
    embedding_service = EmbeddingService()
    
    try:
        results = []
        for doc_id in document_ids:
            try:
                job = db.query(DocumentProcessingJob).filter_by(document_id=doc_id).first()
                if not job or not job.summary:
                    continue
                
                # Генерувати embedding
                import asyncio
                embedding = asyncio.run(embedding_service.embed_text(job.summary))
                
                # Зберегти в БД (якщо є поле для embeddings)
                # job.embedding = embedding
                # db.commit()
                
                results.append({"document_id": doc_id, "status": "success"})
                logger.info(f"Generated embedding for document {doc_id}")
                
            except Exception as e:
                logger.error(f"Error generating embedding for {doc_id}: {e}")
                results.append({"document_id": doc_id, "status": "failed", "error": str(e)})
        
        return {"processed": len(results), "results": results}
        
    finally:
        db.close()


# Періодичні задачі
celery_app.conf.beat_schedule = {
    'cleanup-old-documents-daily': {
        'task': 'services.doc_processor.tasks.cleanup_old_documents',
        'schedule': crontab(hour=3, minute=0),  # Щодня о 3:00
    },
}
