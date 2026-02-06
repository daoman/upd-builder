# UPD Builder - Universal Transfer Document XML Generator

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.9+-green.svg)

Generate valid Russian UPD (Универсальный Передаточный Документ) XML documents compliant with XSD schema v5.03. 

## Features

✅ **XSD Schema Compliant** - Fully compliant with Russian tax authority XSD v5.03  
✅ **Diadoc Ready** - Compatible with Diadoc document exchange system  
✅ **Flexible Configuration** - Support for YAML, JSON, or dictionary-based configs  
✅ **Comprehensive Documentation** - Type hints and docstrings in every method  
✅ **Well-Tested** - Includes unit tests and validation examples  
✅ **Production Ready** - Used in real production environments for tax reporting  

## Installation

### From PyPI
```bash
pip install upd-builder
```

### From Source
```bash
git clone https://github.com/daoman/upd-builder.git
cd upd-builder
pip install -e .
```

## Quick Start

### Basic Usage

```python
from upd_builder import Upd970
import uuid

# Define header information
upd_head = {
    "guid_doc": str(uuid.uuid4()),
    "upd_number": "1",
    "upd_date_yyyymmdd": "20260106",
    "upd_date_russian": "06.01.2026",
    "СтоимВсего": "100000.00",
    "СтоимБезНДСВсего": "100000.00",
    "СумНал": "00.00",
}

# Seller (Поставщик)
upd_seller = {
    "guid": "527634821_527634821",
    "НаимОрг": "ООО \"ТеграМедиа\"",
    "ИНН": "527634821",
    "КПП": "527634821",
    "КодРегион": "78",
    "НаимРегион": "Санкт-Петербург",
    "Индекс": "193284",
    "Улица": "ул Кутузова",
    "Дом": "42",
    "Фамилия": "Морозов",
    "Имя": "Алексей",
    "Отчество": "Сергеевич",
}

# Buyer (Покупатель)
upd_buyer = {
    "guid": "4825367291_482536729",
    "НаимОрг": "ООО \"ДинамикСервис\"",
    "ИНН": "4825367291",
    "КПП": "482536729",
    "КодРегион": "77",
    "НаимРегион": "Москва",
    "Индекс": "125324",
    "Улица": "пл. Ленина",
    "Дом": "д. № 1",
}

# Items/Services
upd_table = [
    {
        "НомСтр": "1",
        "Товар": "Услуга консультирования",
        "ОКЕИ": "796",
        "НаимЕдИзм": "шт",
        "Кол": "1",
        "Цена": "100000.00",
        "СтоимостьБезНДС": "100000.00",
        "Стоимость": "100000.00",
        "НДС": "00.00",
    }
]

# Basis documents
upd_docs = [
    {
        "РеквНаимДок": "Договор об оказании услуг",
        "РеквНомерДок": "123",
        "РеквДатаДок": "01.01.2026",
    }
]

# Generate XML
upd = Upd970(upd_head, upd_buyer, upd_seller, upd_table, upd_docs)
xml_file = upd.create_xml('/path/to/output')
print(f"Generated: {xml_file}")
```

## Configuration Reference

### Header (upd_head)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `guid_doc` | str | ✓ | Document UUID (use `uuid.uuid4()`) |
| `upd_number` | str | ✓ | Document number |
| `upd_date_yyyymmdd` | str | ✓ | Date YYYYMMDD format |
| `upd_date_russian` | str | ✓ | Date DD.MM.YYYY format |
| `СтоимВсего` | str | ✓ | Total cost with VAT |
| `СтоимБезНДСВсего` | str | ✓ | Total cost without VAT |
| `СумНал` | str | ✓ | Total tax amount |
| `ВремИнфПр` | str | | Time (default: "12.00.01") |
| `СодОпер` | str | | Operation description |
| `Должность` | str | | Signer position |
| `КурсВал` | str | | Exchange rate (default: "1.00") |
| `ВидСчета` | str | | Invoice type (default: "Реализация") |

### Organization (Seller/Buyer)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `guid` | str | ✓ | Format: "INN_KPP" |
| `НаимОрг` | str | ✓ | Organization name |
| `ИНН` | str | ✓ | INN (10 or 12 digits) |
| `КПП` | str | | KPP code |
| `КодРегион` | str | ✓ | Region code |
| `НаимРегион` | str | ✓ | Region name |
| `Индекс` | str | | Postal code |
| `Улица` | str | | Street |
| `Дом` | str | | Building number |
| `Корпус` | str | | Building part |
| `Кварт` | str | | Apartment/office |
| `Фамилия` | str | | Signer last name |
| `Имя` | str | | Signer first name |
| `Отчество` | str | | Signer patronymic |
| `БанкРекв` | str | | Account number (seller only) |
| `НаимБанк` | str | | Bank name |
| `БИК` | str | | Bank BIC code |
| `КорСчет` | str | | Correspondent account |

### Items Table (upd_table)

Each item is a dictionary:

```python
{
    "НомСтр": "1",              # Line number
    "Товар": "Product name",    # Product description
    "ОКЕИ": "796",              # OKEI code
    "НаимЕдИзм": "шт",          # Unit name
    "Кол": "1",                 # Quantity
    "Цена": "1000.00",          # Unit price
    "СтоимостьБезНДС": "1000.00",    # Cost without VAT
    "Стоимость": "1000.00",           # Cost with VAT
    "НДС": "00.00",                   # VAT rate or "без НДС"
    "ПрТовРаб": "3",            # Product type (optional)
    "ИД": "uuid",               # Item ID (optional)
}
```

### Basis Documents (upd_docs)

List of documents that serve as basis for this transfer:

```python
{
    "РеквНаимДок": "Contract name",     # Document name
    "РеквНомерДок": "123",              # Document number
    "РеквДатаДок": "01.01.2026",        # Date DD.MM.YYYY
}
```

## Examples

### Example 1: Generate from Dictionary
See `examples/basic_usage.py`

### Example 2: Generate from YAML
See `examples/with_yaml.py` and `examples/sample.yaml`

## Validation

To validate generated XML against XSD schema:

```bash
xmllint --schema ON_NSCHFDOPPR_1_997_01_05_03_04.xsd \
        ON_NSCHFDOPPR__xxx.xml
```

Or using Python:

```python
import xmlschema

schema = xmlschema.XMLSchema('ON_NSCHFDOPPR_1_997_01_05_03_04.xsd')
if schema.is_valid('generated_file.xml'):
    print("✅ Valid!")
else:
    for error in schema.iter_errors('generated_file.xml'):
        print(error)
```

## File Structure

```
upd-builder/
├── upd_builder/
│   ├── __init__.py
│   └── upd_xml.py              # Main Upd970 class
├── examples/
│   ├── basic_usage.py          # Simple example
│   ├── with_yaml.py            # YAML-based example
│   └── sample.yaml             # Config template
├── tests/
│   └── test_upd_builder.py     # Unit tests
├── docs/
│   ├── README.md               # This file
│   └── API.md                  # API reference
├── setup.py                    # Pip package setup
└── LICENSE
```

## Requirements

- Python 3.9+
- No dependencies (uses only stdlib)
- Optional: `ruamel.yaml` for YAML support
- Optional: `xmlschema` for XML validation

## Common Issues

### Issue: "КПП is required for legal entities"
**Solution**: Ensure КПП is provided for 10-digit INNs (legal entities)

### Issue: "Invalid region code"
**Solution**: Use correct region codes:
- 77 = Moscow
- 78 = Saint-Petersburg  
- 50 = Moscow region
- etc.

### Issue: "Date format error"
**Solution**: Use correct formats:
- YYYYMMDD for `upd_date_yyyymmdd` (e.g., "20260106")
- DD.MM.YYYY for `upd_date_russian` (e.g., "06.01.2026")

## Support

- **Documentation**: See `docs/` folder
- **Issues**: Report on GitHub
- **Examples**: See `examples/` folder

## License

MIT License - see LICENSE file for details

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Add tests
4. Submit a pull request

## Changelog

### v1.0.0 (2026-01-06)
- Initial release
- Full XSD v5.03 support
- YAML configuration support
- Comprehensive documentation
- Unit tests included

## Author

Georgy
Email: givi.zurabich@gmail.com

---

**Note**: This library generates Russian tax documents. Ensure compliance with Russian tax authorities' requirements before using in production.
Библиотека генерирует УПД в формате xml в соответствии с принятой схемой. 
