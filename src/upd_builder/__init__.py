"""
UPD (Универсальный Передаточный Документ) XML Builder for Russian Tax Documents

A Python library for generating valid UPD XML files compliant with XSD schema v5.03.
Supports creation of universal transfer documents for Russian tax reporting.
"""

__version__ = "1.0.2"
__author__ = "Georgy"
__license__ = "MIT"

from .upd_xml import Upd970

__all__ = ["Upd970"]
