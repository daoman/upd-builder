"""
UPD (Универсальный Передаточный Документ) XML Generator

Module for creating valid Russian UPD XML documents compliant with XSD schema v5.03.
Supports all required elements and attributes for tax reporting via Diadoc and other systems.

Example:
    >>> upd = Upd970(upd_head, upd_buyer, upd_seller, upd_table, upd_docs)
    >>> upd.create_xml('/path/to/output')
"""

import xml.etree.ElementTree as ET
from datetime import datetime
from typing import Dict, List, Any, Optional


class Upd970:
    """
    Generator for UPD (Universal Transfer Document) XML files.
    
    Attributes:
        head (dict): Document header with dates, numbers, and totals
        buyer (dict): Buyer organization details
        seller (dict): Seller organization details
        table (list): List of goods/services items
        docs (list): List of basis documents (основание передачи)
    """

    def __init__(self, head: Dict[str, Any], buyer: Dict[str, Any], 
                 seller: Dict[str, Any], table: List[Dict[str, Any]], 
                 docs: List[Dict[str, Any]]) -> None:
        """
        Initialize UPD970 document builder.
        
        Args:
            head (dict): Document header information
                - upd_date_yyyymmdd (str): Date in format YYYYMMDD
                - upd_date_russian (str): Date in format DD.MM.YYYY
                - upd_number (str): Document number
                - guid_doc (str): Unique identifier (UUID)
                - СтоимВсего (str): Total cost with VAT
                - СтоимБезНДСВсего (str): Total cost without VAT
                - СумНал (str): Total tax/VAT amount
                - ВремИнфПр (str, optional): Time of information
                - СодОпер (str, optional): Operation content description
                - Должность (str, optional): Position of signer
                - КурсВал (str, optional): Exchange rate (default "1.00")
                - ВидСчета (str, optional): Invoice type (default "Реализация")
                
            buyer (dict): Buyer organization details
                - guid (str): Buyer GUID (use 'ИНН_КПП' format)
                - НаимОрг (str): Organization name
                - ИНН (str): INN (10 or 12 digits)
                - КПП (str, optional): KPP code
                - ОКПО (str, optional): OKPO code
                - КодРегион (str): Region code
                - НаимРегион (str): Region name
                - Индекс (str): Postal code
                - Улица (str): Street
                - Дом (str): Building number
                - Корпус (str, optional): Building part
                - Кварт (str, optional): Apartment/office number
                
            seller (dict): Seller organization details (same structure as buyer)
                - Also supports БанкРекв, НаимБанк, БИК, КорСчет for bank details
                - Should have Фамилия, Имя, Отчество for signer info
                
            table (list): List of goods/services items
                - Each item dict should contain:
                    - НомСтр (str): Line number
                    - Товар (str): Product name/description
                    - ОКЕИ (str): OKEI code (usually "796" for units)
                    - НаимЕдИзм (str): Unit name (usually "шт")
                    - Кол (str): Quantity
                    - Цена (str): Price per unit
                    - СтоимостьБезНДС (str): Cost without VAT
                    - НДС (str): VAT rate ("без НДС" for non-taxable)
                    - Стоимость (str): Total cost with VAT
                    - ПрТовРаб (str, optional): Product type code (default "3")
                    - ИД (str, optional): Item UUID
                    
            docs (list): List of basis documents for transfer
                - Each item dict should contain:
                    - РеквНаимДок (str): Document name
                    - РеквНомерДок (str): Document number
                    - РеквДатаДок (str): Document date (DD.MM.YYYY)
        """
        self.head = head
        self.buyer = buyer
        self.seller = seller
        self.table = table
        self.docs = docs
        
        # Parse dates
        self.upd_date_yyyymmdd = datetime.strptime(
            head["upd_date_yyyymmdd"], "%Y%m%d"
        ).strftime("%Y%m%d")
        self.upd_date_russian = datetime.strptime(
            head["upd_date_russian"], "%d.%m.%Y"
        ).strftime("%d.%m.%Y")

    def org_info(self, parent: ET.Element, infodict: Dict[str, Any], 
                 is_seller: bool = False) -> None:
        """
        Add organization information to XML element.
        
        Creates СвПрод or СвПокуп element with ИдСв, Адрес, and optional БанкРекв.
        
        Args:
            parent (ET.Element): Parent XML element
            infodict (dict): Organization information dictionary
            is_seller (bool): True if this is seller info (enables bank details)
        """
        # Add ОКПО attribute if available
        if infodict.get("ОКПО"):
            parent.set("ОКПО", infodict["ОКПО"])
        
        # Organization identification section
        sv = ET.SubElement(parent, "ИдСв")
        
        if len(infodict["ИНН"]) == 10:
            # Legal entity
            ET.SubElement(sv, "СвЮЛУч", {
                "НаимОрг": infodict["НаимОрг"],
                "ИННЮЛ": infodict["ИНН"],
                "КПП": infodict.get("КПП", "")
            })
        elif len(infodict["ИНН"]) == 12:
            # Individual entrepreneur
            svul = ET.SubElement(sv, "СвИП", {
                "ИННФЛ": infodict["ИНН"]
            })
            name_parts = infodict["НаимОрг"].split()
            ET.SubElement(svul, "ФИО", {
                "Фамилия": name_parts[0] if len(name_parts) > 0 else "",
                "Имя": name_parts[1] if len(name_parts) > 1 else "",
                "Отчество": name_parts[2] if len(name_parts) > 2 else ""
            })
        
        # Address section
        adr0 = ET.SubElement(parent, "Адрес")
        
        if infodict.get("АдрТекст"):
            # Text-based address (foreign or unstructured)
            ET.SubElement(adr0, "АдрИнф", {
                "КодСтр": infodict.get("КодСтр", "643"),
                "НаимСтран": infodict.get("НаимСтран", "РОССИЯ"),
                "АдрТекст": infodict.get("АдрТекст", "")
            })
        else:
            # Structured Russian address
            fields = ["Индекс", "КодРегион", "НаимРегион", "Район", "Город", 
                     "Улица", "Дом", "Корпус", "Кварт"]
            addr_fields = {}
            for f in fields:
                if infodict.get(f):
                    addr_fields[f] = infodict[f]
            
            ET.SubElement(adr0, "АдрРФ", addr_fields)
        
        # Bank details section (for sellers)
        if is_seller and infodict.get("БанкРекв"):
            bank_acct = ET.SubElement(parent, "БанкРекв", 
                                     {"НомерСчета": infodict.get("БанкРекв", "")})
            if infodict.get("СвБанк"):
                ET.SubElement(bank_acct, "СвБанк", {
                    "НаимБанк": infodict.get("НаимБанк", ""),
                    "БИК": infodict.get("БИК", ""),
                    "КорСчет": infodict.get("КорСчет", "")
                })

    def tovar_info(self, parent: ET.Element) -> None:
        """
        Add goods/services information to table.
        
        Creates СведТов elements for each item and adds totals (ВсегоОпл).
        
        Args:
            parent (ET.Element): Parent XML element (ТаблСчФакт)
        """
        for tov in self.table:
            # Build СведТов attributes
            attrs = {
                "НомСтр": tov.get("НомСтр", "1"),
                "НаимТов": tov.get("Товар", ""),
                "ОКЕИ_Тов": tov.get("ОКЕИ", ""),
                "НаимЕдИзм": tov.get("НаимЕдИзм", "шт"),
                "КолТов": tov.get("Кол", "1"),
                "ЦенаТов": tov.get("Цена", "0.00"),
                "СтТовБезНДС": tov.get("СтоимостьБезНДС", "0.00"),
                "НалСт": ("без НДС" if str(tov.get("НДС", "")).strip() 
                         in ("0", "0.00", "00.00", "") else tov.get("НДС")),
                "СтТовУчНал": tov.get("Стоимость", "0.00")
            }
            
            sv = ET.SubElement(parent, "СведТов", attrs)

            # Additional info sections
            dop = ET.SubElement(sv, "ДопСведТов", 
                               {"ПрТовРаб": tov.get("ПрТовРаб", "3")})
            
            # VAT/Excise section
            akciz = ET.SubElement(sv, "Акциз")
            ET.SubElement(akciz, "БезАкциз").text = "без акциза"

            # Tax amount section
            sumnal = ET.SubElement(sv, "СумНал")
            ET.SubElement(sumnal, "БезНДС").text = "без НДС"

            # Additional technical info
            if tov.get("ИД"):
                ET.SubElement(sv, "ИнфПолФХЖ2", {
                    "Идентиф": "ИД", 
                    "Значен": tov.get("ИД", "")
                })

        # Total row
        totalsum = ET.SubElement(parent, "ВсегоОпл", {
            "СтТовБезНДСВсего": self.head.get("СтоимБезНДСВсего", "0.00"),
            "СтТовУчНалВсего": self.head.get("СтоимВсего", "0.00"),
            "КолНеттоВс": str(len(self.table))
        })
        
        totalsumnal = ET.SubElement(totalsum, "СумНалВсего")
        ET.SubElement(totalsumnal, "БезНДС").text = "без НДС"

    def create_xml(self, path: str) -> str:
        """
        Generate UPD XML file.
        
        Creates a complete UPD XML document structure and saves it to disk
        with Windows-1251 encoding (required for Russian tax systems).
        
        Args:
            path (str): Output directory path
            
        Returns:
            str: Full path to the generated XML file
            
        Raises:
            OSError: If directory cannot be created
            
        Example:
            >>> upd = Upd970(head, buyer, seller, table, docs)
            >>> xml_path = upd.create_xml('/tmp/output')
            >>> print(f"Generated: {xml_path}")
        """
        import os
        
        # Extract identifiers for filename
        h1 = self.buyer["guid"]
        h2 = self.seller["guid"]
        h3 = self.upd_date_yyyymmdd
        h4 = self.head["guid_doc"]
    
        filename = f"ON_NSCHFDOPPR_{h1}_{h2}_{h3}_{h4}_0_0_0_0_0_00"
        
        # Create root element
        root = ET.Element("Файл", {
            "ИдФайл": filename,
            "ВерсФорм": "5.03",
            "ВерсПрог": "1С:Предприятие 8"
        })
        
        # Create Документ element with attributes
        document = ET.SubElement(root, "Документ", {
            "КНД": "1115131",
            "Функция": "ДОП",
            "ПоФактХЖ": "Документ об отгрузке товаров (выполнении работ), "
                       "передаче имущественных прав (документ об оказании услуг)",
            "НаимДокОпр": "Документ об отгрузке товаров (выполнении работ), "
                         "передаче имущественных прав (документ об оказании услуг)",
            "ДатаИнфПр": self.upd_date_russian,
            "ВремИнфПр": self.head.get("ВремИнфПр", "12.00.01"),
            "НаимЭконСубСост": self.seller["НаимОрг"]
        })
        
        # Invoice header (СвСчФакт)
        schf = ET.SubElement(document, "СвСчФакт", {
            "НомерДок": str(self.head.get("upd_number", "")),
            "ДатаДок": self.upd_date_russian
        })
        
        # Seller information
        seller = ET.SubElement(schf, "СвПрод")
        self.org_info(seller, self.seller, is_seller=True)
        
        # Buyer information
        buyer = ET.SubElement(schf, "СвПокуп")
        self.org_info(buyer, self.buyer, is_seller=False)

        # Currency information
        ET.SubElement(schf, "ДенИзм", {
            "КодОКВ": "643",
            "НаимОКВ": "Российский рубль",
            "КурсВал": self.head.get("КурсВал", "1.00")
        })

        # Items table
        main_table = ET.SubElement(document, "ТаблСчФакт")
        self.tovar_info(main_table)

        # Transfer information
        osn_pered = ET.SubElement(document, "СвПродПер")
        pered = ET.SubElement(osn_pered, "СвПер", {
            "СодОпер": self.head.get("СодОпер", "Услуги оказаны в полном объеме"),
            "ВидОпер": "Продажа",
            "ДатаПер": self.upd_date_russian
        })
        
        # Basis documents
        for osn in self.docs:
            attrs = {
                "РеквНаимДок": osn.get("РеквНаимДок", 
                                      osn.get("НаимОсн", osn.get("НаимДок", ""))),
                "РеквНомерДок": osn.get("РеквНомерДок", osn.get("НомОсн", "")),
                "РеквДатаДок": osn.get("РеквДатаДок", 
                                      osn.get("ДатаОсн", self.upd_date_russian))
            }
            ET.SubElement(pered, "ОснПер", attrs)
        
        # Transfer signer info
        svel = ET.SubElement(pered, "СвЛицПер")
        raborg = ET.SubElement(svel, "РабОргПрод", 
                              {"Должность": self.head.get("Должность", 
                                                         "Операционный директор")})
        ET.SubElement(raborg, "ФИО", {
            "Фамилия": self.seller.get("Фамилия", ""),
            "Имя": self.seller.get("Имя", ""),
            "Отчество": self.seller.get("Отчество", "")
        })

        # Document signer
        signer = ET.SubElement(document, "Подписант", {
            "СпосПодтПолном": "4",
            "Должн": self.head.get("Должность", "Операционный директор")
        })
        ET.SubElement(signer, "ФИО", {
            "Фамилия": self.seller.get("Фамилия", ""),
            "Имя": self.seller.get("Имя", ""),
            "Отчество": self.seller.get("Отчество", "")
        })

        # Format and write XML
        tree = ET.ElementTree(root)
        ET.indent(tree, space="  ", level=0)

        # Ensure output directory exists
        if not os.path.isdir(path):
            try:
                os.makedirs(path, exist_ok=True)
            except Exception as e:
                path = os.path.dirname(os.path.realpath(__file__))

        # Write file
        out_file = os.path.join(path, filename + '.xml')
        tree.write(out_file, encoding="windows-1251", xml_declaration=True)
        
        return out_file
