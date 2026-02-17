#!/usr/bin/env python3
"""
Тестовий скрипт для перевірки AI консультанта університету
"""
import requests
import json

# Тестуємо через Docker network (backend:8000)
backend_url = "http://localhost:8002"  # Backend працює на порту 8002

# Спочатку отримаємо список університетів
print("Отримуємо список університетів...")
response = requests.get(f"{backend_url}/api/universities?jurisdiction_code=SK&type=university")
print(f"Status: {response.status_code}")

if response.status_code == 200:
    universities = response.json()['universities']
    if universities:
        first_uni = universities[0]
        uni_id = first_uni['id']
        uni_name = first_uni['name']
        print(f"\n✅ Знайдено університет: {uni_name} (ID: {uni_id})")
        
        # Тепер тестуємо чат
        print(f"\n💬 Тестуємо чат для університету ID {uni_id}...")
        chat_payload = {
            "message": "Які документи треба для вступу?",
            "session_id": "test_session_123"
        }
        
        print(f"Відправляємо запит на: {backend_url}/api/universities/{uni_id}/chat")
        print(f"Payload: {json.dumps(chat_payload, ensure_ascii=False)}")
        
        try:
            chat_response = requests.post(
                f"{backend_url}/api/universities/{uni_id}/chat",
                json=chat_payload,
                headers={"Content-Type": "application/json"},
                timeout=30
            )
            
            print(f"\n📊 Статус відповіді: {chat_response.status_code}")
            print(f"📝 Заголовки відповіді: {dict(chat_response.headers)}")
            
            if chat_response.status_code == 200:
                data = chat_response.json()
                print(f"\n✅ УСПІХ! Отримано відповідь:")
                print(f"Response: {data.get('response', 'N/A')}")
                print(f"Session ID: {data.get('session_id', 'N/A')}")
            else:
                print(f"\n❌ ПОМИЛКА! Код: {chat_response.status_code}")
                print(f"Текст помилки: {chat_response.text}")
                
        except Exception as e:
            print(f"\n❌ ВИНЯТОК при виклику чату: {e}")
            import traceback
            traceback.print_exc()
    else:
        print("❌ Університети не знайдені")
else:
    print(f"❌ Помилка при отриманні університетів: {response.status_code}")
