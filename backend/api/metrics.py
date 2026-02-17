#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
University Chat Metrics Endpoint
Provides monitoring and metrics for university chat system
"""

from fastapi import APIRouter, Depends
from typing import Dict
from services.university_chat_service import UniversityChatService
from api.university_chat import get_chat_service

router = APIRouter(
    prefix="/api/metrics",
    tags=["metrics"]
)


# Global metrics storage (in production, use Redis or similar)
_global_metrics = {
    "total_requests": 0,
    "successful_requests": 0,
    "failed_requests": 0,
    "rag_hits": 0,
    "rag_misses": 0,
    "web_searches": 0,
    "total_tokens_used": 0,
    "total_cost_usd": 0.0
}


@router.get("/university-chat")
def get_university_chat_metrics(
    chat_service: UniversityChatService = Depends(get_chat_service)
) -> Dict:
    """
    Get metrics for university chat system
    
    Returns:
        Dict with metrics including:
        - Request counts (total, successful, failed)
        - RAG performance (hits, misses, hit rate)
        - OpenAI usage (tokens, cost)
        - Success rate
    """
    return chat_service.get_metrics()


@router.get("/university-chat/summary")
def get_metrics_summary(
    chat_service: UniversityChatService = Depends(get_chat_service)
) -> Dict:
    """
    Get summary of key metrics
    
    Returns:
        Dict with high-level metrics for dashboard
    """
    metrics = chat_service.get_metrics()
    
    return {
        "status": "healthy" if metrics["success_rate"] > 0.95 else "degraded",
        "total_requests": metrics["total_requests"],
        "success_rate_percent": round(metrics["success_rate"] * 100, 2),
        "rag_hit_rate_percent": round(metrics["rag_hit_rate"] * 100, 2),
        "total_cost_usd": round(metrics["total_cost_usd"], 2),
        "avg_cost_per_request_usd": round(metrics["avg_cost_per_request"], 4)
    }


@router.post("/university-chat/reset")
def reset_metrics(
    chat_service: UniversityChatService = Depends(get_chat_service)
) -> Dict:
    """
    Reset metrics (admin only - add auth in production)
    
    Returns:
        Confirmation message
    """
    chat_service.metrics = {
        "total_requests": 0,
        "successful_requests": 0,
        "failed_requests": 0,
        "rag_hits": 0,
        "rag_misses": 0,
        "web_searches": 0,
        "total_tokens_used": 0,
        "total_cost_usd": 0.0
    }
    
    return {"message": "Metrics reset successfully"}
