from services.jobs_chat_service import JobsChatService

service = JobsChatService()

# Test city extraction
message = "Hladam brigadu v Košice"
city = service._extract_city_from_message(message, 'SK')

print(f"Message: '{message}'")
print(f"Detected city: {city}")

if city:
    # Test RAG context retrieval
    from main import SessionLocal
    db = SessionLocal()
    
    context = service._get_agencies_context(db, city, 'SK')
    print(f"\nRAG Context length: {len(context)} chars")
    print(f"\nRAG Context preview:")
    print(context[:500])
    
    db.close()
else:
    print("\nERROR: City not detected!")
