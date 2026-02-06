"""
Unit tests for UPD Builder

Run with: pytest tests/
"""

import pytest
import tempfile
import os
import uuid
from pathlib import Path
from xml.etree import ElementTree as ET

from upd_builder import Upd970


class TestUpd970Init:
    """Test Upd970 initialization"""
    
    def get_sample_data(self):
        """Return sample data for testing"""
        return {
            "head": {
                "guid_doc": str(uuid.uuid4()),
                "upd_number": "1",
                "upd_date_yyyymmdd": "20260106",
                "upd_date_russian": "06.01.2026",
                "СтоимВсего": "100000.00",
                "СтоимБезНДСВсего": "100000.00",
                "СумНал": "00.00",
            },
            "seller": {
                "guid": "612347589_612347589",
                "НаимОрг": "ООО \"ИнноваСофт\"",
                "ИНН": "612347589",
                "КПП": "612347589",
                "КодРегион": "78",
                "НаимРегион": "Санкт-Петербург",
                "Индекс": "196105",
                "Улица": "ул Тестовая",
                "Дом": "1",
            },
            "buyer": {
                "guid": "3847562910_384756291",
                "НаимОрг": "ООО \"БизнесЛайн\"",
                "ИНН": "3847562910",
                "КПП": "384756291",
                "КодРегион": "77",
                "НаимРегион": "Москва",
                "Индекс": "125047",
                "Улица": "ул Примерная",
                "Дом": "33",
            },
            "table": [
                {
                    "НомСтр": "1",
                    "Товар": "Услуга",
                    "ОКЕИ": "796",
                    "НаимЕдИзм": "шт",
                    "Кол": "1",
                    "Цена": "100000.00",
                    "СтоимостьБезНДС": "100000.00",
                    "Стоимость": "100000.00",
                    "НДС": "00.00",
                }
            ],
            "docs": [
                {
                    "РеквНаимДок": "Договор",
                    "РеквНомерДок": "123",
                    "РеквДатаДок": "01.01.2026",
                }
            ]
        }
    
    def test_init_success(self):
        """Test successful initialization"""
        data = self.get_sample_data()
        upd = Upd970(
            data["head"], 
            data["buyer"], 
            data["seller"], 
            data["table"], 
            data["docs"]
        )
        assert upd.head == data["head"]
        assert upd.upd_date_yyyymmdd == "20260106"
        assert upd.upd_date_russian == "06.01.2026"
    
    def test_date_parsing(self):
        """Test date parsing"""
        data = self.get_sample_data()
        upd = Upd970(
            data["head"],
            data["buyer"],
            data["seller"],
            data["table"],
            data["docs"]
        )
        assert upd.upd_date_yyyymmdd == "20260106"
        assert upd.upd_date_russian == "06.01.2026"


class TestXmlGeneration:
    """Test XML file generation"""
    
    def get_sample_data(self):
        """Return sample data for testing"""
        return {
            "head": {
                "guid_doc": str(uuid.uuid4()),
                "upd_number": "1",
                "upd_date_yyyymmdd": "20260106",
                "upd_date_russian": "06.01.2026",
                "СтоимВсего": "100000.00",
                "СтоимБезНДСВсего": "100000.00",
                "СумНал": "00.00",
            },
            "seller": {
                "guid": "847562341_847562341",
                "НаимОрг": "ООО \"КвантумТех\"",
                "ИНН": "847562341",
                "КПП": "847562341",
                "КодРегион": "78",
                "НаимРегион": "Санкт-Петербург",
                "Индекс": "196235",
                "Улица": "ул Тестовая",
                "Дом": "1",
                "Фамилия": "Занин",
                "Имя": "Игорь",
                "Отчество": "Викторович",
            },
            "buyer": {
                "guid": "5674928103_567492810",
                "НаимОрг": "ООО \"ВектораПлюс\"",
                "ИНН": "5674928103",
                "КПП": "567492810",
                "КодРегион": "77",
                "НаимРегион": "Москва",
                "Индекс": "122347",
                "Улица": "ул Примерная",
                "Дом": "1",
            },
            "table": [
                {
                    "НомСтр": "1",
                    "Товар": "Услуга",
                    "ОКЕИ": "796",
                    "НаимЕдИзм": "шт",
                    "Кол": "1",
                    "Цена": "100000.00",
                    "СтоимостьБезНДС": "100000.00",
                    "Стоимость": "100000.00",
                    "НДС": "00.00",
                }
            ],
            "docs": [
                {
                    "РеквНаимДок": "Договор",
                    "РеквНомерДок": "123",
                    "РеквДатаДок": "01.01.2026",
                }
            ]
        }
    
    def test_xml_generation(self):
        """Test XML file is created"""
        data = self.get_sample_data()
        upd = Upd970(
            data["head"],
            data["buyer"],
            data["seller"],
            data["table"],
            data["docs"]
        )
        
        with tempfile.TemporaryDirectory() as tmpdir:
            xml_file = upd.create_xml(tmpdir)
            assert os.path.exists(xml_file)
            assert xml_file.endswith('.xml')
    
    def test_xml_structure(self):
        """Test generated XML has correct structure"""
        data = self.get_sample_data()
        upd = Upd970(
            data["head"],
            data["buyer"],
            data["seller"],
            data["table"],
            data["docs"]
        )
        
        with tempfile.TemporaryDirectory() as tmpdir:
            xml_file = upd.create_xml(tmpdir)
            tree = ET.parse(xml_file)
            root = tree.getroot()
            
            # Check root element
            assert "Файл" in root.tag
            assert root.get("ВерсФорм") == "5.03"
            
            # Check Документ element exists
            doc_found = False
            for child in root:
                if "Документ" in child.tag:
                    doc_found = True
                    break
            assert doc_found, "Документ element not found"
    
    def test_multiple_items(self):
        """Test XML generation with multiple items"""
        data = self.get_sample_data()
        data["table"] = [
            {
                "НомСтр": "1",
                "Товар": "Услуга 1",
                "ОКЕИ": "796",
                "НаимЕдИзм": "шт",
                "Кол": "2",
                "Цена": "50000.00",
                "СтоимостьБезНДС": "100000.00",
                "Стоимость": "100000.00",
                "НДС": "00.00",
            },
            {
                "НомСтр": "2",
                "Товар": "Услуга 2",
                "ОКЕИ": "796",
                "НаимЕдИзм": "шт",
                "Кол": "1",
                "Цена": "50000.00",
                "СтоимостьБезНДС": "50000.00",
                "Стоимость": "50000.00",
                "НДС": "00.00",
            }
        ]
        
        upd = Upd970(
            data["head"],
            data["buyer"],
            data["seller"],
            data["table"],
            data["docs"]
        )
        
        with tempfile.TemporaryDirectory() as tmpdir:
            xml_file = upd.create_xml(tmpdir)
            assert os.path.exists(xml_file)


class TestEdgeCases:
    """Test edge cases and error handling"""
    
    def test_individual_entrepreneur(self):
        """Test with individual entrepreneur (12-digit INN)"""
        head = {
            "guid_doc": str(uuid.uuid4()),
            "upd_number": "1",
            "upd_date_yyyymmdd": "20260106",
            "upd_date_russian": "06.01.2026",
            "СтоимВсего": "1000.00",
            "СтоимБезНДСВсего": "1000.00",
            "СумНал": "00.00",
        }
        
        ip_seller = {
            "guid": "348567294021_781001001",
            "НаимОрг": "Петрович Дмитрий Сергеевич",
            "ИНН": "348567294021",  # 12 digits
            "КодРегион": "78",
            "НаимРегион": "Санкт-Петербург",
            "Индекс": "196105",
            "Улица": "ул Тестовая",
            "Дом": "1",
            "Фамилия": "Петрович",
            "Имя": "Дмитрий",
            "Отчество": "Сергеевич",
        }
        
        buyer = {
            "guid": "5674928103_567492810",
            "НаимОрг": "ООО \"ВектораПлюс\"",
            "ИНН": "5674928103",
            "КПП": "567492810",
            "КодРегион": "77",
            "НаимРегион": "Москва",
            "Индекс": "125047",
            "Улица": "ул Примерная",
            "Дом": "33",
        }
        
        table = [{
            "НомСтр": "1",
            "Товар": "Услуга",
            "ОКЕИ": "796",
            "НаимЕдИзм": "шт",
            "Кол": "1",
            "Цена": "1000.00",
            "СтоимостьБезНДС": "1000.00",
            "Стоимость": "1000.00",
            "НДС": "00.00",
        }]
        
        docs = [{
            "РеквНаимДок": "Договор",
            "РеквНомерДок": "1",
            "РеквДатаДок": "01.01.2026",
        }]
        
        upd = Upd970(head, buyer, ip_seller, table, docs)
        
        with tempfile.TemporaryDirectory() as tmpdir:
            xml_file = upd.create_xml(tmpdir)
            assert os.path.exists(xml_file)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
