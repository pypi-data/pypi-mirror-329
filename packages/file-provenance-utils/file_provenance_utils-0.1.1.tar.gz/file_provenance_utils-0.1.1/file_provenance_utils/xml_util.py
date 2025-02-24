import logging
import os
import socket
import sys

from datetime import datetime

import xml.etree.ElementTree as ET
from xml.dom import minidom


def get_provenance(**kwargs) -> str:
    """Retrieve provenance information to be inserted into XML output file.

    Args:
        **kwargs: Arbitrary keyword arguments.

    Returns:
        str: The provenance information in XML format.
    """
    logging.info(
        f"Will attempt to derive the provenance information to be inserted into an XML file."
    )

    # Create the root element for XML
    root = ET.Element("provenance")

    # Retrieve and set the executable
    executable = kwargs.get("executable", os.path.abspath(sys.argv[0]))
    executable_elem = ET.SubElement(root, "executable")
    executable_elem.text = executable

    # Retrieve and set the config file (if provided)
    config_file = kwargs.get("config_file", None)
    if config_file is not None:
        config_file_elem = ET.SubElement(root, "config_file")
        config_file_elem.text = config_file

    # Retrieve and set the logfile (if provided)
    logfile = kwargs.get("logfile", None)
    if logfile is not None:
        logfile_elem = ET.SubElement(root, "logfile")
        logfile_elem.text = logfile

    # Retrieve and set the datetime
    date_created = kwargs.get("date-created", None)
    if date_created is None:
        date_created = datetime.today().strftime("%Y-%m-%d %H:%M:%S")

    date_created_elem = ET.SubElement(root, "date-created")
    date_created_elem.text = date_created

    # Retrieve and set the host
    host = kwargs.get("host", socket.gethostname())
    host_elem = ET.SubElement(root, "host")
    host_elem.text = host

    # Retrieve and set the user
    user = kwargs.get(
        "user", os.getenv("USER") or os.getenv("USERNAME") or "unknown-user"
    )
    user_elem = ET.SubElement(root, "user")
    user_elem.text = user

    # Retrieve and set the output directory (if provided)
    outdir = kwargs.get("outdir", None)
    if outdir is not None:
        outdir_elem = ET.SubElement(root, "outdir")
        outdir_elem.text = outdir

    # Retrieve and set the files (if provided)
    files = kwargs.get("files", None)
    if files is not None:
        files_elem = ET.SubElement(root, "files")
        for file_name, filepath in files.items():
            file_elem = ET.SubElement(files_elem, "file")
            file_elem.set("name", file_name)
            file_elem.text = os.path.abspath(filepath)

    # # Generate the XML string
    # tree = ET.ElementTree(root)
    # from io import StringIO
    # xml_str = StringIO()
    # tree.write(xml_str, encoding="unicode", xml_declaration=True)
    # return xml_str.getvalue()

    # Generate the XML string
    tree = ET.ElementTree(root)
    from io import StringIO

    xml_str = StringIO()
    tree.write(xml_str, encoding="unicode", xml_declaration=True)

    # Parse the string and pretty print it
    xml_str.seek(0)
    pretty_xml = minidom.parseString(xml_str.getvalue()).toprettyxml(indent="    ")

    return pretty_xml
