"""Top-level package for File Provenance Utils."""

__author__ = """Jaideep Sundaram"""
__email__ = "jai.python3@gmail.com"
__version__ = "0.1.0"

from file_provenance_utils.plain_text_util import (
    get_provenance as get_plain_text_provenance,
)
from file_provenance_utils.json_util import get_provenance as get_json_provenance
from file_provenance_utils.xml_util import get_provenance as get_xml_provenance
