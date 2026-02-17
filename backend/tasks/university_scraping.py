#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
University Scraping Tasks
Celery tasks for scraping universities and generating embeddings
"""

from celery_app import celery_app
from sqlalchemy.orm import Session
import asyncio


# Global engine (singleton pattern)
_engine = None
_SessionLocal = None

def get_db_session():
    """Get database session for Celery tasks"""
    global _engine, _SessionLocal
    
    if _engine is None:
        from sqlalchemy import create_engine
        from sqlalchemy.orm import sessionmaker
        import os
        
        DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://user:password@db:5432/codex_db')
        _engine = create_engine(DATABASE_URL, pool_pre_ping=True)
        _SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=_engine)
    
    return _SessionLocal()



@celery_app.task(name="scrape_university")
def scrape_university_task(university_id: int):
    """
    Scrape single university website
    
    Args:
        university_id: University ID to scrape
    """
    db = get_db_session()
    try:
        from tasks.models import University, UniversityScrapingStatus
        from services.university_scraper import UniversityScraper
        from services.embedding_service import EmbeddingService
        
        # Get university
        university = db.query(University).filter_by(id=university_id).first()
        if not university or not university.website_url:
            print(f"University {university_id} not found or has no website")
            return {'success': False, 'error': 'No website'}
        
        # Scrape university
        scraper = UniversityScraper(db)
        result = asyncio.run(scraper.scrape_university(
            university_id=university_id,
            website_url=university.website_url
        ))
        
        if not result['success']:
            return result
        
        # Generate embeddings for scraped content
        from tasks.models import UniversityContent
        content_items = db.query(UniversityContent).filter_by(
            university_id=university_id
        ).all()
        
        content_ids = [item.id for item in content_items]
        
        if content_ids:
            embedding_service = EmbeddingService()
            embedding_result = asyncio.run(
                embedding_service.batch_generate_embeddings(db, content_ids)
            )
            
            # Update scraping status
            status = db.query(UniversityScrapingStatus).filter_by(
                university_id=university_id
            ).first()
            
            if status:
                status.embeddings_generated = embedding_result['success_count']
                db.commit()
            
            result['embeddings'] = embedding_result
        
        return result
        
    except Exception as e:
        db.rollback()  # Rollback failed transaction
        print(f"Error in scrape_university_task: {e}")
        return {'success': False, 'error': str(e)}
    finally:
        db.close()


@celery_app.task(name="scrape_all_universities")
def scrape_all_universities_task():
    """Scrape all universities that need scraping"""
    db = get_db_session()
    try:
        from tasks.models import University, UniversityScrapingStatus
        
        # Get universities that need scraping
        universities = db.query(University).filter_by(is_active=True).all()
        
        scraped_count = 0
        for university in universities:
            # Check if needs scraping
            status = db.query(UniversityScrapingStatus).filter_by(
                university_id=university.id
            ).first()
            
            if not status or status.scraping_status in ['pending', 'failed']:
                # Queue scraping task
                scrape_university_task.delay(university.id)
                scraped_count += 1
        
        return {
            'success': True,
            'queued': scraped_count,
            'total': len(universities)
        }
        
    except Exception as e:
        print(f"Error in scrape_all_universities_task: {e}")
        return {'success': False, 'error': str(e)}
    finally:
        db.close()


@celery_app.task(name="scrape_pending_universities")
def scrape_pending_universities_task(limit: int = 10):
    """
    Scrape universities with pending status
    
    Args:
        limit: Maximum number of universities to scrape
    """
    db = get_db_session()
    try:
        from tasks.models import UniversityScrapingStatus
        
        # Get pending universities
        pending = db.query(UniversityScrapingStatus).filter_by(
            scraping_status='pending'
        ).limit(limit).all()
        
        for status in pending:
            scrape_university_task.delay(status.university_id)
        
        return {
            'success': True,
            'queued': len(pending)
        }
        
    except Exception as e:
        print(f"Error in scrape_pending_universities_task: {e}")
        return {'success': False, 'error': str(e)}
    finally:
        db.close()


@celery_app.task(name="generate_embeddings_for_university")
def generate_embeddings_task(university_id: int):
    """
    Generate embeddings for university content
    
    Args:
        university_id: University ID
    """
    db = get_db_session()
    try:
        from tasks.models import UniversityContent
        from services.embedding_service import EmbeddingService
        
        # Get content without embeddings
        content_items = db.query(UniversityContent).filter_by(
            university_id=university_id,
            is_active=True
        ).all()
        
        content_ids = [item.id for item in content_items]
        
        if not content_ids:
            return {'success': True, 'message': 'No content to process'}
        
        # Generate embeddings
        embedding_service = EmbeddingService()
        result = asyncio.run(
            embedding_service.batch_generate_embeddings(db, content_ids)
        )
        
        return result
        
    except Exception as e:
        print(f"Error in generate_embeddings_task: {e}")
        return {'success': False, 'error': str(e)}
    finally:
        db.close()
