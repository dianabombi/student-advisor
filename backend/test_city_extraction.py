from services.jobs_chat_service import JobsChatService

service = JobsChatService()

# Test city extraction
test_messages = [
    "ladam brigadu v Košice",
    "práca v Košiciach",
    "work in Košice",
    "Шукаю роботу в Кошицях",
    "в Кошице",
]

print("Testing city extraction:")
print("="*60)

for msg in test_messages:
    city = service._extract_city_from_message(msg, 'SK')
    print(f"Message: '{msg}'")
    print(f"Detected city: {city}")
    print()
