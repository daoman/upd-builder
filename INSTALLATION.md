# UPD Builder Package - Installation & Usage Guide

## 📦 Package Structure

```
upd-builder/
├── upd_builder/
│   ├── __init__.py              # Package initialization
│   └── upd_xml.py               # Main Upd970 class (228 lines)
├── examples/
│   ├── basic_usage.py           # Simple example
│   ├── with_yaml.py             # YAML-based example
│   └── sample.yaml              # Configuration template
├── tests/
│   ├── __init__.py
│   └── test_upd_builder.py      # Unit tests (~250 lines)
├── setup.py                     # Setup configuration for pip
├── pyproject.toml               # Modern Python packaging
├── README.md                    # Full documentation
├── CONTRIBUTING.md              # Contribution guidelines
├── LICENSE                      # MIT License
├── MANIFEST.in                  # Additional files for package
└── .gitignore                   # Git ignore rules
```

## 🚀 Installation

### Option 1: Install from Source (Development)

```bash
cd upd-builder
pip install -e .
```

### Option 2: Install with All Features

```bash
# For YAML support
pip install -e ".[yaml]"

# For XML validation
pip install -e ".[validation]"

# For development (includes all + dev tools)
pip install -e ".[dev]"
```

### Option 3: Prepare for PyPI Distribution

```bash
# Install build tools
pip install build twine

# Build the package
python -m build

# Upload to PyPI (after registering)
twine upload dist/*
```

## 📖 Quick Start

### 1. Import and Use

```python
from upd_builder import Upd970
import uuid

# Prepare data
head = {..."upd_number": "1", ...}
buyer = {...}
seller = {...}
table = [{...}]
docs = [{...}]

# Generate
upd = Upd970(head, buyer, seller, table, docs)
xml_file = upd.create_xml('/output/path')

print(f"✅ Generated: {xml_file}")
```

### 2. Run Examples

```bash
# Basic example
python examples/basic_usage.py

# YAML-based example
python examples/with_yaml.py
```

### 3. Run Tests

```bash
# Install test dependencies
pip install -e ".[dev]"

# Run all tests
pytest tests/

# With coverage report
pytest tests/ --cov=upd_builder --cov-report=html
```

## 🔧 Available Options

### Installation extras (in setup.py or pyproject.toml):

```
[yaml]      - ruamel.yaml>=0.17.0
[validation] - xmlschema>=2.0.0
[dev]       - All of above + testing & linting tools
```

### Environment Variables

No specific environment variables needed. Just ensure Python 3.9+ is installed.

## 📝 Configuration Fields

### Header Information (upd_head)
```python
{
    "guid_doc": str(uuid.uuid4()),
    "upd_number": "1",                          # Document number
    "upd_date_yyyymmdd": "20260106",           # YYYYMMDD format
    "upd_date_russian": "06.01.2026",          # DD.MM.YYYY format
    "СтоимВсего": "100000.00",                 # Total with VAT
    "СтоимБезНДСВсего": "100000.00",          # Total without VAT
    "СумНал": "00.00",                         # Total tax
}
```

### Organization Information
```python
{
    "guid": "78132234335_7221314401",    # INN_КПП format
    "НаимОрг": "ООО \"Ромашка\"",     # Organization name
    "ИНН": "78132234335",               # 10 (entity) or 12 (IP) digits
    "КПП": "7221314401",                # For entities
    "КодРегион": "78",                 # Region code
    "НаимРегион": "Санкт-Петербург",   # Region name
    "Индекс": "196155",                # Postal code
    "Улица": "ул Думская",           # Street
    "Дом": "1",                        # Building
    "Кварт": "1",                      # Office/apartment (optional)
}
```

### Goods/Services Items
```python
{
    "НомСтр": "1",                     # Line number
    "Товар": "Услуга",                 # Product description
    "ОКЕИ": "796",                     # OKEI code
    "НаимЕдИзм": "шт",                 # Unit name
    "Кол": "1",                        # Quantity
    "Цена": "100000.00",               # Unit price
    "СтоимостьБезНДС": "100000.00",   # Cost without VAT
    "Стоимость": "100000.00",         # Total cost with VAT
    "НДС": "00.00",                    # NDS or "без НДС"
}
```

## 📋 Complete YAML Example

See [examples/sample.yaml](examples/sample.yaml) for a complete working configuration:

```yaml
# Sample configuration for UPD generation
# You can use this file as a template for your own UPD documents

upd_head:
  guid_doc: "640aa2da-fd1f-11f0-958b-fa163ed74eee"
  upd_number: "5"
  upd_date_yyyymmdd: "20260106"
  upd_date_russian: "06.01.2026"
  СтоимВсего: "5050.00"
  СтоимБезНДСВсего: "5050.00"
  СумНал: "00.00"
  ВремИнфПр: "12.00.01"
  СодОпер: "Услуги оказаны в полном объеме"
  Должность: "Генеральный директор"
  КурсВал: "1.00"
  ВидСчета: "Реализация"

upd_seller:
  guid: "78132234335_7221314401"
  НаимОрг: "ООО \"Ромашка\""
  ИНН: "78132234335"
  КПП: "7221314401"
  ОКПО: "23123105"
  КодРегион: "78"
  НаимРегион: "Город Санкт-Петербург"
  Город: "Санкт-Петербург"
  Индекс: "196155"
  Улица: "ул Думская"
  Дом: "1"
  Корпус: "1"
  Кварт: "1"
  Фамилия: "Иванов"
  Имя: "Иван"
  Отчество: "Иванович"
  БанкРекв: "407022343243242343244"
  НаимБанк: "ФИЛИАЛ БЕТА-БАНКА"
  БИК: "0440234324"
  КорСчет: "301018123432423423423"

upd_buyer:
  guid: "7723432423_723423423"
  НаимОрг: "ООО \"КУЛЕР\""
  ИНН: "7723432423"
  КПП: "723423423"
  КодРегион: "77"
  НаимРегион: "Город Москва"
  Город: "Москва"
  Индекс: "125444"
  Улица: "пл. Ленина"
  Дом: "д. № 1"
  Корпус: "стр. 1"
  Кварт: "помещ. 1"

upd_table:
  - НомСтр: "1"
    Товар: "Носки кружевные"
    ОКЕИ: "796"
    НаимЕдИзм: "шт"
    Кол: "10"
    Цена: "500.00"
    СтоимостьБезНДС: "500.00"
    Стоимость: "500.00"
    НДС: "00.00"
    ПрТовРаб: "3"
    ИД: "640aa2da-fd1f-11f0-958b-fa163ed74eee"
  - НомСтр: "2"
    Товар: "Носки разные"
    ОКЕИ: "796"
    НаимЕдИзм: "шт"
    Кол: "5"
    Цена: "10.00"
    СтоимостьБезНДС: "10.00"
    Стоимость: "10.00"
    НДС: "00.00"
    ПрТовРаб: "3"
    ИД: "4d65fd9a-fd1f-11f0-958b-fa163ed74eee"

upd_docs:
  - РеквНаимДок: "Дог/1 от 09.12.2018"
    РеквНомерДок: "Дог/1"
    РеквДатаДок: "09.12.2018"
```

**Usage with this configuration:**

```bash
python examples/with_yaml.py
```

## ✅ Features

✨ **XSD Compliant** - Fully validates against v5.03 schema  
🔒 **Type Hints** - Full Python type annotations  
📚 **Documented** - Comprehensive docstrings and examples  
🧪 **Tested** - Unit tests included  
🎯 **Production Ready** - Used in real tax reporting systems  
⚙️ **Configurable** - YAML, JSON, or dict-based configs  

## 🐛 Troubleshooting

### Common Issues

**KPP is required for legal entities**
- Ensure КПП is provided for 10-digit INNs

**Invalid region code**
- Use correct region codes (77=Moscow, 78=SPB, etc.)

**Date format error**
- Use YYYYMMDD for `upd_date_yyyymmdd`
- Use DD.MM.YYYY for `upd_date_russian`

### Getting Help

1. Check [README.md](README.md) for API reference
2. Look at [examples/](examples/) for usage patterns
3. Review [tests/](tests/) for test cases
4. Open an issue on GitHub

## 🔗 Integration Examples

### With Django/Flask

```python
from upd_builder import Upd970

def generate_upd_for_invoice(invoice_id):
    invoice = Invoice.objects.get(id=invoice_id)
    
    upd_head = {...}
    upd = Upd970(upd_head, invoice.buyer, invoice.seller, 
                 invoice.items, invoice.basis_docs)
    
    return upd.create_xml('/tmp/udp_output')
```

### With Celery (Async Tasks)

```python
from celery import shared_task
from upd_builder import Upd970

@shared_task
def generate_upd_async(config_data):
    upd = Upd970(config_data['head'], config_data['buyer'],
                 config_data['seller'], config_data['table'],
                 config_data['docs'])
    
    xml_file = upd.create_xml(config_data['output_dir'])
    return xml_file
```

## 📄 License

MIT License - Use freely in commercial and personal projects.

## 👨‍💻 Author

Georgy
Email: givi.zurabuch@gmail.com  
GitHub: [upd-builder](https://github.com/yourusername/upd-builder)

---

**Ready to generate UPD documents? Start with the examples above!** 🎉
