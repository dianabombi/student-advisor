from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from pydantic import BaseModel
import json
import os
from openai import OpenAI

router = APIRouter()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# These will be injected by main.py
get_db = None
get_current_user = None

# Language mapping for jurisdictions
JURISDICTION_LANGUAGES = {
    'SK': 'Slovak',      # Slovakia
    'CZ': 'Czech',       # Czech Republic
    'PL': 'Polish',      # Poland
    'UA': 'Ukrainian',   # Ukraine
    'RU': 'Russian',     # Russia
    'DE': 'German',      # Germany
    'AT': 'German',      # Austria
    'IT': 'Italian',     # Italy
    'FR': 'French',      # France
    'ES': 'Spanish',     # Spain
    'GB': 'English',     # United Kingdom
    'US': 'English',     # United States
}

def detect_user_language(user, db):
    """
    Detect user's preferred language from jurisdiction or profile
    """
    # Try to get user's jurisdiction
    try:
        from main import Jurisdiction
        # Check if user has jurisdiction_id or similar field
        if hasattr(user, 'jurisdiction_id') and user.jurisdiction_id:
            jurisdiction = db.query(Jurisdiction).filter_by(id=user.jurisdiction_id).first()
            if jurisdiction and jurisdiction.code in JURISDICTION_LANGUAGES:
                return JURISDICTION_LANGUAGES[jurisdiction.code]
        
        # Fallback: check if user has language preference
        if hasattr(user, 'language') and user.language:
            return user.language.capitalize()
        
        # Default to English
        return 'English'
    except:
        return 'English'

def get_language_instruction(language):
    """
    Get AI instruction for responding in specific language
    """
    instructions = {
        'Slovak': 'Respond ONLY in Slovak language (slovenčina)',
        'Czech': 'Respond ONLY in Czech language (čeština)',
        'Polish': 'Respond ONLY in Polish language (polski)',
        'Ukrainian': 'Respond ONLY in Ukrainian language (українська)',
        'Russian': 'Respond ONLY in Russian language (русский)',
        'German': 'Respond ONLY in German language (Deutsch)',
        'Italian': 'Respond ONLY in Italian language (italiano)',
        'French': 'Respond ONLY in French language (français)',
        'Spanish': 'Respond ONLY in Spanish language (español)',
        'English': 'Respond ONLY in English language',
    }
    return instructions.get(language, 'Respond in English language')

class SupportRequest(BaseModel):
    issue_description: str

@router.post("/api/support/analyze-issue")
async def analyze_user_issue(
    request: SupportRequest,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    AI analyzes user's problem based on their logs
    """
    from main import logger
    
    # 1. Collect user's logs from last hour
    one_hour_ago = datetime.now() - timedelta(hours=1)
    
    logs = []
    try:
        with open('/app/logs/codex.log', 'r') as f:
            for line in f:
                try:
                    log_entry = json.loads(line)
                    # Filter by user_id and timestamp
                    if (log_entry.get('user_id') == current_user.id and 
                        log_entry.get('timestamp', '') > one_hour_ago.isoformat()):
                        logs.append(log_entry)
                except:
                    continue
    except FileNotFoundError:
        logs = []
    
    # 2. Prepare context for AI
    recent_logs = logs[-50:]  # Last 50 entries
    
    # Find errors
    errors = [log for log in recent_logs if log.get('level') == 'error']
    
    # Find API calls
    api_calls = [log for log in recent_logs if log.get('event') == 'api_request']
    
    # Find OpenAI calls
    openai_calls = [log for log in recent_logs if 'openai' in log.get('event', '')]
    
    # 3. Load knowledge base
    knowledge_base = ""
    try:
        with open('/app/ai_support_knowledge.txt', 'r', encoding='utf-8') as f:
            knowledge_base = f.read()
    except:
        knowledge_base = "No knowledge base available"
    
    # 4. Detect user's language from jurisdiction/preference
    user_language = detect_user_language(current_user, db)
    language_instruction = get_language_instruction(user_language)
    
    # 5. Create prompt for AI
    prompt = f"""
You are an AI Support Agent for Student platform (educational platform for university applications).

USER'S PROBLEM:
{request.issue_description}

USER INFORMATION:
- User ID: {current_user.id}
- Email: {current_user.email}
- Plan: {getattr(current_user, 'subscription_plan', 'basic')}
- Requests used: {getattr(current_user, 'requests_used_this_month', 0)}/{getattr(current_user, 'monthly_request_limit', 500)}
- Language: {user_language}

LOGS FROM LAST HOUR:

Errors ({len(errors)}):
{json.dumps(errors, indent=2, ensure_ascii=False)}

API calls ({len(api_calls)}):
{json.dumps(api_calls[-10:], indent=2, ensure_ascii=False)}

OpenAI calls ({len(openai_calls)}):
{json.dumps(openai_calls[-5:], indent=2, ensure_ascii=False)}

KNOWLEDGE BASE:
{knowledge_base}

TASK:
1. Analyze logs and find the root cause
2. Give clear explanation of what went wrong
3. Provide specific steps to solve the problem
4. If it's not user's fault (e.g. OpenAI down) - mention it
5. {language_instruction}

FORMAT:
- Short and clear
- Numbered steps
- If upgrade needed - mention it
- If technical issue - suggest contacting support
"""

    # 5. Get AI response
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a professional AI Support Agent. Help users solve problems quickly."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )
        
        ai_response = response.choices[0].message.content
    except Exception as e:
        logger.error("ai_support_error", error=str(e))
        raise HTTPException(status_code=500, detail="AI support temporarily unavailable")
    
    # 6. Log AI support interaction
    logger.info("ai_support_response",
               user_id=current_user.id,
               issue=request.issue_description,
               errors_found=len(errors),
               response_length=len(ai_response))
    
    # 7. Save to database
    from main import SupportTicket
    support_ticket = SupportTicket(
        user_id=current_user.id,
        issue_description=request.issue_description,
        ai_response=ai_response,
        logs_analyzed=len(recent_logs),
        errors_found=len(errors),
        status="ai_resolved",
        needs_human=len(errors) > 5,
        created_at=datetime.now()
    )
    db.add(support_ticket)
    db.commit()
    
    return {
        "response": ai_response,
        "logs_analyzed": len(recent_logs),
        "errors_found": len(errors),
        "ticket_id": support_ticket.id,
        "needs_human_support": len(errors) > 5
    }

@router.get("/api/admin/support/tickets")
async def get_support_tickets(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Get all support tickets (admin only)
    """
    # TODO: Add admin role check
    from main import SupportTicket
    
    tickets = db.query(SupportTicket).order_by(SupportTicket.created_at.desc()).limit(100).all()
    
    return {
        "tickets": [
            {
                "id": t.id,
                "user": {"email": t.user.email if t.user else "Unknown"},
                "issue_description": t.issue_description,
                "ai_response": t.ai_response,
                "errors_found": t.errors_found,
                "needs_human": t.needs_human,
                "status": t.status,
                "created_at": t.created_at.isoformat()
            }
            for t in tickets
        ]
    }
