# 📈 Маркетингова Аналітика CODEX - Інструкція

## Що Це Таке?

Маркетингова аналітика дозволяє відстежувати ефективність ваших рекламних кампаній та розраховувати ключові метрики:
- **ROI** (Return on Investment) - повернення інвестицій по каналах
- **CAC** (Customer Acquisition Cost) - вартість залучення клієнта
- **Ефективність кампаній** - детальний аналіз кожної рекламної кампанії
- **Порівняння каналів** - який канал працює найкраще

## Нові API Ендпоінти

### 1. 💰 ROI по Каналах

**GET** `/api/owner/analytics/marketing/roi?days=30`

Показує ROI для кожного маркетингового каналу.

**Приклад відповіді:**
```json
{
  "channels": [
    {
      "channel": "google_ads",
      "cost": 50000,  // 500 EUR
      "revenue": 120000,  // 1200 EUR
      "profit": 70000,  // 700 EUR
      "roi": 140.0,  // 140% ROI
      "roas": 2.4,  // Return on Ad Spend
      "conversions": 12,
      "visitors": 450,
      "conversion_rate": 2.67
    },
    {
      "channel": "facebook_ads",
      "cost": 30000,
      "revenue": 80000,
      "profit": 50000,
      "roi": 166.67,
      "roas": 2.67,
      "conversions": 8,
      "visitors": 320,
      "conversion_rate": 2.5
    }
  ]
}
```

**Що означають метрики:**
- `roi` - ROI у відсотках (140% = на кожен 1 EUR витрат отримали 1.40 EUR прибутку)
- `roas` - Return on Ad Spend (2.4 = на кожен 1 EUR витрат отримали 2.4 EUR виторгу)
- `conversion_rate` - відсоток відвідувачів що стали платними клієнтами

### 2. 💵 CAC (Customer Acquisition Cost)

**GET** `/api/owner/analytics/marketing/cac?days=30`

Розраховує вартість залучення одного клієнта.

**Приклад відповіді:**
```json
{
  "total_marketing_cost": 80000,  // 800 EUR
  "paid_customers": 20,
  "total_registrations": 87,
  "cac_paid_customers": 4000,  // 40 EUR за платного клієнта
  "cac_all_users": 919,  // 9.19 EUR за реєстрацію
  "average_ltv": 12000,  // 120 EUR середній LTV
  "ltv_cac_ratio": 3.0,  // LTV:CAC = 3:1
  "is_healthy": true  // Здоровий бізнес якщо > 3
}
```

**Що означають метрики:**
- `cac_paid_customers` - скільки коштує залучити одного платного клієнта
- `average_ltv` - середній виторг від одного клієнта (Lifetime Value)
- `ltv_cac_ratio` - співвідношення LTV до CAC (має бути > 3 для здорового бізнесу)
- `is_healthy` - чи здоровий ваш бізнес (true якщо LTV > 3x CAC)

### 3. 📊 Ефективність Рекламних Кампаній

**GET** `/api/owner/analytics/marketing/campaigns?days=30`

Детальний аналіз кожної рекламної кампанії.

**Приклад відповіді:**
```json
{
  "campaigns": [
    {
      "campaign_id": 1,
      "campaign_name": "Winter Sale 2025",
      "channel": "google_ads",
      "utm_campaign": "winter2025",
      "utm_source": "google",
      "cost": 50000,
      "visitors": 450,
      "registrations": 45,
      "paid_subscriptions": 12,
      "revenue": 120000,
      "profit": 70000,
      "roi": 140.0,
      "cpa": 4166,  // Cost Per Acquisition (41.66 EUR)
      "cpc": 111,  // Cost Per Click (1.11 EUR)
      "conversion_rate": 2.67,
      "is_active": true
    }
  ],
  "total_campaigns": 5
}
```

**Що означають метрики:**
- `cpa` - Cost Per Acquisition (скільки коштує залучити одного платного клієнта)
- `cpc` - Cost Per Click/Visit (скільки коштує один візит)
- `conversion_rate` - відсоток відвідувачів що стали платними клієнтами

### 4. 🔍 Порівняння Каналів

**GET** `/api/owner/analytics/marketing/channel-comparison?days=30`

Порівняння ефективності різних маркетингових каналів.

**Приклад відповіді:**
```json
{
  "best_channel": {
    "name": "facebook_ads",
    "roi": 166.67,
    "revenue": 80000,
    "cost": 30000
  },
  "worst_channel": {
    "name": "linkedin_ads",
    "roi": 50.0,
    "revenue": 30000,
    "cost": 20000
  },
  "channels": [...],  // Всі канали відсортовані по ROI
  "total_channels": 4
}
```

## Управління Кампаніями

### ➕ Створити Кампанію

**POST** `/api/owner/analytics/marketing/campaigns/create`

Додає нову маркетингову кампанію для відстеження.

**Приклад запиту:**
```json
{
  "campaign_name": "Winter Sale 2025",
  "utm_campaign": "winter2025",
  "utm_source": "google",
  "utm_medium": "cpc",
  "channel": "google_ads",
  "cost": 50000,  // 500 EUR в центах
  "start_date": "2025-12-01T00:00:00",
  "end_date": "2025-12-31T23:59:59",
  "notes": "Рекламна кампанія на зимовий розпродаж"
}
```

**Приклад відповіді:**
```json
{
  "message": "Campaign created successfully",
  "campaign_id": 1,
  "campaign_name": "Winter Sale 2025"
}
```

### 📋 Список Кампаній

**GET** `/api/owner/analytics/marketing/campaigns/list`

Отримує список всіх маркетингових кампаній.

**Приклад відповіді:**
```json
{
  "campaigns": [
    {
      "id": 1,
      "campaign_name": "Winter Sale 2025",
      "utm_campaign": "winter2025",
      "utm_source": "google",
      "utm_medium": "cpc",
      "channel": "google_ads",
      "cost": 50000,
      "start_date": "2025-12-01T00:00:00",
      "end_date": "2025-12-31T23:59:59",
      "is_active": true,
      "created_at": "2025-11-25T10:00:00"
    }
  ],
  "total": 5
}
```

## Як Використовувати

### Крок 1: Створіть Кампанію

Перед запуском реклами, створіть кампанію в системі:

```bash
curl -X POST "http://localhost:8001/api/owner/analytics/marketing/campaigns/create" \
  -H "Authorization: Bearer ВАШ_ТОКЕН" \
  -H "Content-Type: application/json" \
  -d '{
    "campaign_name": "Facebook Winter Sale",
    "utm_campaign": "winter2025",
    "utm_source": "facebook",
    "utm_medium": "cpc",
    "channel": "facebook_ads",
    "cost": 30000,
    "start_date": "2025-12-01T00:00:00",
    "end_date": "2025-12-31T23:59:59"
  }'
```

### Крок 2: Використовуйте UTM Параметри

Додайте UTM параметри до ваших рекламних посилань:

```
https://yourcodex.com/?utm_source=facebook&utm_medium=cpc&utm_campaign=winter2025
```

Система автоматично відстежить всіх відвідувачів з цієї кампанії.

### Крок 3: Аналізуйте Результати

Після запуску кампанії, перевіряйте її ефективність:

```bash
# ROI по каналах
curl -X GET "http://localhost:8001/api/owner/analytics/marketing/roi?days=30" \
  -H "Authorization: Bearer ВАШ_ТОКЕН"

# CAC
curl -X GET "http://localhost:8001/api/owner/analytics/marketing/cac?days=30" \
  -H "Authorization: Bearer ВАШ_ТОКЕН"

# Ефективність кампаній
curl -X GET "http://localhost:8001/api/owner/analytics/marketing/campaigns?days=30" \
  -H "Authorization: Bearer ВАШ_ТОКЕН"
```

## Приклад Використання в Python

```python
import requests

token = "ВАШ_ТОКЕН"
headers = {"Authorization": f"Bearer {token}"}
base_url = "http://localhost:8001/api/owner/analytics"

# 1. Створити кампанію
campaign_data = {
    "campaign_name": "Google Ads Q1 2025",
    "utm_campaign": "q1_2025",
    "utm_source": "google",
    "utm_medium": "cpc",
    "channel": "google_ads",
    "cost": 100000,  # 1000 EUR
    "start_date": "2025-01-01T00:00:00",
    "end_date": "2025-03-31T23:59:59"
}

response = requests.post(
    f"{base_url}/marketing/campaigns/create",
    headers=headers,
    json=campaign_data
)
print(f"Кампанія створена: {response.json()}")

# 2. Отримати ROI по каналах
roi_response = requests.get(
    f"{base_url}/marketing/roi?days=30",
    headers=headers
)
roi_data = roi_response.json()

for channel in roi_data['channels']:
    print(f"\nКанал: {channel['channel']}")
    print(f"  Витрати: {channel['cost']/100} EUR")
    print(f"  Виторг: {channel['revenue']/100} EUR")
    print(f"  ROI: {channel['roi']}%")
    print(f"  Конверсія: {channel['conversion_rate']}%")

# 3. Розрахувати CAC
cac_response = requests.get(
    f"{base_url}/marketing/cac?days=30",
    headers=headers
)
cac_data = cac_response.json()

print(f"\n=== CAC Аналіз ===")
print(f"Витрати на маркетинг: {cac_data['total_marketing_cost']/100} EUR")
print(f"Платних клієнтів: {cac_data['paid_customers']}")
print(f"CAC: {cac_data['cac_paid_customers']/100} EUR")
print(f"LTV: {cac_data['average_ltv']/100} EUR")
print(f"LTV:CAC Ratio: {cac_data['ltv_cac_ratio']}")
print(f"Здоровий бізнес: {'✅ Так' if cac_data['is_healthy'] else '❌ Ні'}")

# 4. Найефективніші кампанії
campaigns_response = requests.get(
    f"{base_url}/marketing/campaigns?days=30",
    headers=headers
)
campaigns_data = campaigns_response.json()

print(f"\n=== Топ 3 Кампанії ===")
for i, campaign in enumerate(campaigns_data['campaigns'][:3], 1):
    print(f"\n{i}. {campaign['campaign_name']}")
    print(f"   ROI: {campaign['roi']}%")
    print(f"   Виторг: {campaign['revenue']/100} EUR")
    print(f"   Конверсія: {campaign['conversion_rate']}%")
```

## Ключові Метрики

### ROI (Return on Investment)
```
ROI = (Revenue - Cost) / Cost × 100%
```
- **Добре**: ROI > 100% (заробили більше ніж витратили)
- **Погано**: ROI < 0% (втратили гроші)

### ROAS (Return on Ad Spend)
```
ROAS = Revenue / Cost
```
- **Добре**: ROAS > 3 (на кожен 1 EUR витрат отримали 3 EUR виторгу)
- **Мінімум**: ROAS > 1 (окупність)

### CAC (Customer Acquisition Cost)
```
CAC = Total Marketing Cost / Number of Customers
```
- **Добре**: CAC < LTV / 3 (LTV:CAC ratio > 3)
- **Погано**: CAC > LTV (втрачаємо гроші на кожному клієнті)

### LTV:CAC Ratio
```
LTV:CAC = Lifetime Value / Customer Acquisition Cost
```
- **Відмінно**: > 5
- **Добре**: 3-5
- **Прийнятно**: 1-3
- **Погано**: < 1

## Поради

1. **Відстежуйте всі кампанії** - створюйте запис для кожної рекламної кампанії
2. **Використовуйте UTM параметри** - завжди додавайте їх до рекламних посилань
3. **Аналізуйте ROI** - зупиняйте кампанії з негативним ROI
4. **Оптимізуйте CAC** - знижуйте вартість залучення клієнта
5. **Порівнюйте канали** - інвестуйте більше в найефективніші канали
6. **Стежте за LTV:CAC** - має бути > 3 для здорового бізнесу

---

**Створено для платформи CODEX**
**Версія: 1.0**
**Дата: 21.12.2025**
