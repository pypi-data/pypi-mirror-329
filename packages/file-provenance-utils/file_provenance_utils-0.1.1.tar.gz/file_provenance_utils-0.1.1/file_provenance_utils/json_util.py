import logging
import os
import socket
import sys

from datetime import datetime

from typing import Any, Dict


def get_provenance(**kwargs) -> Dict[str, Any]:
    """Retrieve provenance information to be inserted into JSON output file.

    Args:
        **kwargs: Arbitrary keyword arguments.

    Returns:
        Dict[str, Any]: The provenance information.
    """
    logging.info(
        f"Will attempt to derive the provenance information to be inserted into a JSON file."
    )

    contents = {}

    executable = kwargs.get("executable", os.path.abspath(sys.argv[0]))
    contents["executable"] = executable

    config_file = kwargs.get("config_file", None)
    if config_file is not None:
        contents["config_file"] = config_file

    logfile = kwargs.get("logfile", None)
    if logfile is not None:
        contents["logfile"] = logfile

    date_created = kwargs.get("date-created", None)
    if date_created is None:
        date_created = datetime.today().strftime("%Y-%m-%d %H:%M:%S")

    contents["date-created"] = date_created

    host = kwargs.get("host", socket.gethostname())
    contents["host"] = host

    user = kwargs.get(
        "user", os.getenv("USER") or os.getenv("USERNAME") or "unknown-user"
    )
    contents["user"] = user

    outdir = kwargs.get("outdir", None)
    if outdir is not None:
        contents["outdir"] = outdir

    files = kwargs.get("files", None)
    if files is not None:
        contents["files"] = {}
        for file_name, filepath in files.items():
            contents["files"][file_name] = os.path.abspath(filepath)

    return {"provenance": contents}
