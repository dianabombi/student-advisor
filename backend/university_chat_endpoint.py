

@app.post("/api/universities/{university_id}/chat")
async def chat_with_university(
    university_id: int,
    chat_request: UniversityChatRequest,
    db: Session = Depends(get_db)
):
    """
    Chat with AI about a specific university using RAG
    Returns AI-generated responses based on scraped university data
    """
    # Verify university exists
    university = db.query(University).filter_by(id=university_id, is_active=True).first()
    if not university:
        raise HTTPException(status_code=404, detail="University not found")
    
    # Get or create session
    session_id = chat_request.session_id
    if not session_id:
        session_id = f"univ_{university_id}_{datetime.utcnow().timestamp()}_{os.urandom(4).hex()}"
    
    # Get existing session or create new one
    chat_session = db.query(UniversityChatSession).filter_by(
        university_id=university_id,
        is_active=True
    ).first()
    
    if not chat_session:
        chat_session = UniversityChatSession(
            university_id=university_id,
            user_id=None,  # Anonymous for now
            messages=[],
            context={"university_name": university.name},
            is_active=True
        )
        db.add(chat_session)
        db.commit()
    
    # Add user message to history
    user_message = {
        "role": "user",
        "content": chat_request.message,
        "timestamp": datetime.utcnow().isoformat()
    }
    
    messages = chat_session.messages or []
    messages.append(user_message)
    
    # TODO: Integrate with RAG/AI Service
    # For now, return a placeholder response
    ai_response_text = f"Thank you for your question about {university.name}. This is a placeholder response. RAG integration coming soon."
    
    # In production, this would be:
    # ai_response_text = await query_university_rag(university_id, chat_request.message, messages)
    
    # Add AI response to history
    ai_message = {
        "role": "assistant",
        "content": ai_response_text,
        "timestamp": datetime.utcnow().isoformat()
    }
    messages.append(ai_message)
    
    # Update session
    chat_session.messages = messages
    chat_session.session_ended = datetime.utcnow()
    db.commit()
    
    return UniversityChatResponse(
        response=ai_response_text,
        session_id=session_id
    )


@app.get("/api/universities/{university_id}/chat/history")
def get_chat_history(
    university_id: int,
    session_id: str,
    db: Session = Depends(get_db)
):
    """Get chat history for a specific session"""
    chat_session = db.query(UniversityChatSession).filter_by(
        university_id=university_id,
        is_active=True
    ).first()
    
    if not chat_session:
        return {"messages": []}
    
    return {"messages": chat_session.messages or []}
