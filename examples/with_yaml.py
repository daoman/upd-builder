"""
Example: Generate UPD from YAML configuration

This example demonstrates loading UPD parameters from YAML file
and generating the XML document.
"""

from upd_builder import Upd970
from ruamel.yaml import YAML
import os

# Load configuration from YAML
yaml = YAML(typ='safe')
config_path = os.path.join(os.path.dirname(__file__), 'sample.yaml')

with open(config_path, 'r', encoding='utf-8') as f:
    cfg = yaml.load(f)

# Extract components from config
upd_head = cfg['upd_head']
upd_buyer = cfg['upd_buyer']
upd_seller = cfg['upd_seller']
upd_table = cfg['upd_table']
upd_docs = cfg['upd_docs']

# Generate UPD XML
upd = Upd970(upd_head, upd_buyer, upd_seller, upd_table, upd_docs)
xml_file = upd.create_xml('/tmp/upd_output')

print(f"✅ UPD generated from YAML config!")
print(f"📄 File: {xml_file}")
print(f"📋 Items: {len(upd_table)}")
print(f"💰 Total: {upd_head['СтоимВсего']}")
