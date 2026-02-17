# Document Types and Fields Reference

## Supported Document Types

CODEX platform supports **25+ document types** across 5 categories:

### 📄 Contracts (Zmluvy)
1. **Employment Contract** (`employment_contract`) - Pracovná zmluva
2. **Purchase Agreement** (`purchase_agreement`) - Kúpna zmluva
3. **Lease Agreement** (`lease_agreement`) - Nájomná zmluva
4. **Service Contract** (`service_contract`) - Zmluva o poskytovaní služieb
5. **Work Contract** (`work_contract`) - Zmluva o dielo
6. **Loan Agreement** (`loan_agreement`) - Zmluva o pôžičke

### 💰 Financial Documents (Finančné doklady)
7. **Invoice** (`invoice`) - Faktúra
8. **Receipt** (`receipt`) - Potvrdenie o prijatí
9. **Payment Order** (`payment_order`) - Platobný príkaz

### ⚖️ Legal Documents (Právne dokumenty)
10. **Power of Attorney** (`power_of_attorney`) - Plná moc
11. **Court Decision** (`court_decision`) - Súdne rozhodnutie
12. **Lawsuit** (`lawsuit`) - Žaloba
13. **Complaint** (`complaint`) - Sťažnosť

### 📋 Administrative Documents (Administratívne dokumenty)
14. **Act** (`act`) - Akt/Protokol
15. **Protocol** (`protocol`) - Protokol
16. **Certificate** (`certificate`) - Osvedčenie
17. **Permit** (`permit`) - Povolenie

### 📧 Correspondence (Korešpondencia)
18. **Letter** (`letter`) - List
19. **Email** (`email`) - Email
20. **Notice** (`notice`) - Oznámenie

### 📝 Other (Ostatné)
21. **Application** (`application`) - Žiadosť
22. **Statement** (`statement`) - Vyhlásenie
23. **Other** (`other`) - Iné

---

## Field Definitions by Document Type

### 1. Employment Contract (Pracovná zmluva)

**Required Fields:**
- `contract_number` - Číslo zmluvy
- `contract_date` - Dátum uzavretia
- `employer` - Zamestnávateľ
- `employee` - Zamestnanec
- `position` - Pracovná pozícia
- `salary` - Mzda
- `start_date` - Dátum nástupu

**Optional Fields:**
- `contract_type` - Typ zmluvy (určitý/neurčitý čas)

**Example:**
```json
{
  "contract_number": "ZML-001/2024",
  "contract_date": "15.12.2024",
  "employer": "ABC s.r.o.",
  "employee": "Ján Novák",
  "position": "Programátor",
  "salary": "2000 EUR",
  "start_date": "01.01.2025",
  "contract_type": "neurčitý čas"
}
```

---

### 2. Purchase Agreement (Kúpna zmluva)

**Required Fields:**
- `contract_number` - Číslo zmluvy
- `contract_date` - Dátum uzavretia
- `seller` - Predávajúci
- `buyer` - Kupujúci
- `purchase_price` - Kúpna cena
- `subject` - Predmet kúpy

**Optional Fields:**
- `payment_terms` - Platobné podmienky

---

### 3. Lease Agreement (Nájomná zmluva)

**Required Fields:**
- `contract_number` - Číslo zmluvy
- `contract_date` - Dátum uzavretia
- `lessor` - Prenajímateľ
- `lessee` - Nájomca
- `property_address` - Adresa nehnuteľnosti
- `monthly_rent` - Mesačné nájomné
- `lease_period` - Doba nájmu

**Optional Fields:**
- `deposit` - Kaucia

---

### 4. Invoice (Faktúra)

**Required Fields:**
- `invoice_number` - Číslo faktúry
- `invoice_date` - Dátum vystavenia
- `due_date` - Dátum splatnosti
- `supplier` - Dodávateľ
- `customer` - Odberateľ
- `total_amount` - Celková suma

**Optional Fields:**
- `vat_amount` - DPH
- `supplier_ico` - IČO dodávateľa
- `supplier_dic` - DIČ dodávateľa

**Example:**
```json
{
  "invoice_number": "FA-123/2024",
  "invoice_date": "01.12.2024",
  "due_date": "15.12.2024",
  "supplier": "XYZ s.r.o.",
  "customer": "ABC a.s.",
  "total_amount": "1200 EUR",
  "vat_amount": "240 EUR",
  "supplier_ico": "12345678",
  "supplier_dic": "1234567890"
}
```

---

### 5. Power of Attorney (Plná moc)

**Required Fields:**
- `document_date` - Dátum vyhotovenia
- `principal` - Splnomocniteľ
- `attorney` - Splnomocnenec
- `scope` - Rozsah splnomocnenia

**Optional Fields:**
- `validity_period` - Doba platnosti

---

### 6. Court Decision (Súdne rozhodnutie)

**Required Fields:**
- `case_number` - Spisová značka
- `decision_date` - Dátum rozhodnutia
- `court_name` - Názov súdu
- `plaintiff` - Žalobca
- `defendant` - Žalovaný

**Optional Fields:**
- `decision_type` - Typ rozhodnutia (Rozsudok/Uznesenie)

---

### 7. Act (Akt/Protokol)

**Required Fields:**
- `act_number` - Číslo aktu
- `act_date` - Dátum vyhotovenia
- `act_type` - Typ aktu
- `parties` - Účastníci
- `subject` - Predmet aktu

---

### 8. Letter (List)

**Required Fields:**
- `letter_date` - Dátum listu
- `sender` - Odosielateľ
- `recipient` - Príjemca

**Optional Fields:**
- `subject` - Predmet
- `reference_number` - Číslo jednania

---

### 9. Application (Žiadosť)

**Required Fields:**
- `application_date` - Dátum podania
- `applicant` - Žiadateľ
- `recipient_authority` - Príslušný orgán
- `application_type` - Typ žiadosti
- `subject` - Predmet žiadosti

---

## Field Types

### Available Field Types:

- **TEXT** - Textové pole
- **DATE** - Dátum
- **AMOUNT** - Suma (peňažná)
- **PERSON** - Osoba (meno)
- **ORGANIZATION** - Organizácia
- **ADDRESS** - Adresa
- **IDENTIFIER** - Identifikátor (IČO, DIČ, číslo zmluvy)
- **PERIOD** - Obdobie (od-do)
- **BOOLEAN** - Áno/Nie

---

## Usage Examples

### Get Document Fields

```python
from services.doc_processor.document_types import (
    DocumentType,
    get_document_fields,
    get_required_fields
)

# Get all fields for employment contract
fields = get_document_fields(DocumentType.EMPLOYMENT_CONTRACT)

for field in fields:
    print(f"{field.name}: {field.description}")
    print(f"  Type: {field.field_type}")
    print(f"  Required: {field.required}")
```

### Get Required Fields Only

```python
required = get_required_fields(DocumentType.INVOICE)

print(f"Invoice requires {len(required)} fields:")
for field in required:
    print(f"- {field.name}: {field.description}")
```

### Get Document Type Info

```python
from services.doc_processor.document_types import get_document_type_info

info = get_document_type_info()

for doc_type, details in info.items():
    print(f"{doc_type}:")
    print(f"  Total fields: {details['total_fields']}")
    print(f"  Required: {', '.join(details['required_fields'])}")
```

### Validate Extracted Data

```python
from services.doc_processor.document_types import (
    DocumentType,
    get_required_fields
)

# Extracted data
extracted = {
    'contract_number': 'ZML-001/2024',
    'contract_date': '15.12.2024',
    'employer': 'ABC s.r.o.'
    # Missing: employee, position, salary, start_date
}

# Check required fields
required = get_required_fields(DocumentType.EMPLOYMENT_CONTRACT)
missing = []

for field in required:
    if field.name not in extracted:
        missing.append(field.name)

if missing:
    print(f"Missing required fields: {', '.join(missing)}")
```

---

## Adding New Document Types

To add a new document type:

1. Add enum value to `DocumentType`
2. Define fields in `DOCUMENT_FIELDS` dictionary
3. Specify required/optional fields
4. Add examples and descriptions

**Example:**

```python
# 1. Add to DocumentType enum
class DocumentType(str, Enum):
    # ...
    RENTAL_CONTRACT = "rental_contract"

# 2. Define fields
DOCUMENT_FIELDS[DocumentType.RENTAL_CONTRACT] = [
    FieldDefinition(
        name="contract_number",
        field_type=FieldType.IDENTIFIER,
        required=True,
        description="Číslo zmluvy"
    ),
    # ... more fields
]
```

---

## Statistics

- **Total Document Types**: 23
- **Average Fields per Type**: 6-8
- **Total Unique Fields**: 50+
- **Languages Supported**: Slovak, Czech, English

---

**Last Updated**: 2025-12-04  
**Version**: 1.0
