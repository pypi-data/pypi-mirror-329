import logging
import os
import socket
import sys

from datetime import datetime


def get_provenance(**kwargs) -> str:
    """Retrieve provenance information to be inserted into plain text output file.

    This might be for a tab-delimited or comma-separated or plain text file.

    Args:
        **kwargs: Arbitrary keyword arguments.

    Returns:
        str: The provenance information.
    """
    logging.info(
        f"Will attempt to derive the provenance information to be inserted into a plain text file."
    )

    contents = []

    executable = kwargs.get("executable", os.path.abspath(sys.argv[0]))
    contents.append(f"executable: {executable}")

    config_file = kwargs.get("config_file", None)
    if config_file is not None:
        contents.append(f"config_file: {config_file}")

    logfile = kwargs.get("logfile", None)
    if logfile is not None:
        contents.append(f"logfile: {logfile}")

    date_created = kwargs.get("date-created", None)
    if date_created is None:
        date_created = datetime.today().strftime("%Y-%m-%d %H:%M:%S")
    contents.append(f"date-created: {date_created}")

    host = kwargs.get("host", socket.gethostname())
    contents.append(f"host: {host}")

    user = kwargs.get(
        "user", os.getenv("USER") or os.getenv("USERNAME") or "unknown-user"
    )
    contents.append(f"user: {user}")

    outdir = kwargs.get("outdir", None)
    if outdir is not None:
        contents.append(f"outdir: {outdir}")

    files = kwargs.get("files", None)
    if files is not None:
        contents.append("files:")
        # from pprint import pprint
        # pprint(files)
        # # sys.exit(1)
        for file_name, filepath in files.items():
            contents.append(f"{file_name}: {os.path.abspath(filepath)}")

    prefixed_contents = [f"## {content}" for content in contents]
    return "\n".join(prefixed_contents)
