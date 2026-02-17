from city_detect import _extract_city_from_message_multilingual

# Test with user's actual message
test_messages = [
    "ladam brigadu v Košice",
    "Шукаю роботу в Кошицях",
    "в Кошице",
    "work in Kosice",
    "praca w Koszycach",
    "práce v Košicích",
    "Arbeit in Kaschau",
    "trabajo en Košice",
]

print("Testing multilingual city detection:")
print("="*60)

for msg in test_messages:
    city = _extract_city_from_message_multilingual(msg)
    print(f"'{msg}' -> {city}")
