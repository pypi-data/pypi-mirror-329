# file-provenance-utils
Collection of functions for deriving provenance information for insertion into the output files.

This will include:
- The absolute path for the primary executable.
- The timestamp for when the file was created.
- The user account that generated the output file.
- The host/server that the software was executed on.


- [file-provenance-utils](#file-provenance-utils)
  - [Use Cases](#use-cases)
  - [Class Diagrams](#class-diagrams)
  - [Installation](#installation)
  - [Usage](#usage)
    - [For JSON output files:](#for-json-output-files)
    - [For tab-delimited files:](#for-tab-delimited-files)
  - [Contributing](#contributing)
  - [To-Do/Coming Next](#to-docoming-next)
  - [CHANGELOG](#changelog)
  - [License](#license)


## Installation

Please see the [INSTALL](docs/INSTALL.md) guide for instructions.

## Usage

### Example code [example/json_example.py](examples/json_example.py) for writing JSON output file:


```python
from file_provenance_utils import get_json_provenance

outfile = "/tmp/test-file-provenance-utils/report.json"

config_file = "config.yaml"
logfile = "/tmp/analysis.log"
outdir = "/tmp/test-file-provenance-utils/instance-outdir"
files = {
    "input_file": "/tmp/test-file-provenance-utils/instance-input-file.txt",
    "data1_file": "/tmp/test-file-provenance-utils/data1-file.txt",
    "data2_file": "/tmp/test-file-provenance-utils/data2-file.txt"
}

provenance = get_json_provenance(
    config_file=config_file,
    logfile=logfile,
    outdir=outdir,
    files=files
)

# Assuming the provenance returned is a dictionary and needs to be serialized to JSON
import json
with open(outfile, "w") as f:
    json.dump(provenance, f, indent=4)

print(f"Wrote provenance information to: {outfile}")
```

### Contents of output JSON file:

```json
{
    "provenance": {
        "executable": "/tmp/test-file-provenance-utils/json_example.py",
        "config_file": "config.yaml",
        "logfile": "/tmp/analysis.log",
        "date-created": "2025-02-23 15:41:01",
        "host": "r2d2",
        "user": "sundaram",
        "outdir": "/tmp/test-file-provenance-utils/instance-outdir",
        "files": {
            "input_file": "/tmp/test-file-provenance-utils/instance-input-file.txt",
            "data1_file": "/tmp/test-file-provenance-utils/data1-file.txt",
            "data2_file": "/tmp/test-file-provenance-utils/data2-file.txt"
        }
    }
}
```

### Example code [example/xml_example.py](examples/xml_example.py) for writing XML output file:

```python
from file_provenance_utils import get_xml_provenance

outfile = "/tmp/test-file-provenance-utils/report.xml"

config_file = "config.yaml"
logfile = "/tmp/analysis.log"
outdir = "/tmp/test-file-provenance-utils/instance-outdir"
files = {
    "input_file": "/tmp/test-file-provenance-utils/instance-input-file.txt",
    "data1_file": "/tmp/test-file-provenance-utils/data1-file.txt",
    "data2_file": "/tmp/test-file-provenance-utils/data2-file.txt"
}

provenance = get_xml_provenance(
    config_file=config_file,
    logfile=logfile,
    outdir=outdir,
    files=files
)

# Write the XML string directly to the output file
with open(outfile, "w") as f:
    f.write(provenance)

print(f"Wrote provenance information to: {outfile}")
```

### Contents of output XML file:

```xml
<?xml version="1.0" ?>
<provenance>
    <executable>/tmp/test-file-provenance-utils/xml_example.py</executable>
    <config_file>config.yaml</config_file>
    <logfile>/tmp/analysis.log</logfile>
    <date-created>2025-02-23 15:45:55</date-created>
    <host>r2d2</host>
    <user>sundaram</user>
    <outdir>/tmp/test-file-provenance-utils/instance-outdir</outdir>
    <files>
        <file name="input_file">/tmp/test-file-provenance-utils/instance-input-file.txt</file>
        <file name="data1_file">/tmp/test-file-provenance-utils/data1-file.txt</file>
        <file name="data2_file">/tmp/test-file-provenance-utils/data2-file.txt</file>
    </files>
</provenance>
```


### Example code [example/plain_text_example.py](examples/plain_text_example.py) for writing tab-delimited or comma-separated or plain text output file:


```python
from file_provenance_utils import get_plain_text_provenance

outfile = "/tmp/test-file-provenance-utils/report.txt"
config_file = "config.yaml"
logfile = "/tmp/analysis.log"
outdir = "/tmp/test-file-provenance-utils/instance-outdir"
files = {
    "input_file": "/tmp/test-file-provenance-utils/instance-input-file.txt",
    "data1_file": "/tmp/test-file-provenance-utils/data1-file.txt",
    "data2_file": "/tmp/test-file-provenance-utils/data2-file.txt"
}

provenance = get_plain_text_provenance(
    config_file=config_file,
    logfile=logfile,
    outdir=outdir,
    files=files
)
with open(outfile, "w") as f:
    f.write(provenance)

print(f"Wrote provenance information to: {outfile}")
```

### Contents of output plain-text file:

```text
## executable: /tmp/test-file-provenance-utils/plain_text_example.py
## config_file: config.yaml
## logfile: /tmp/analysis.log
## date-created: 2025-02-23 15:40:52
## host: r2d2
## user: sundaram
## outdir: /tmp/test-file-provenance-utils/instance-outdir
## files:
## input_file: /tmp/test-file-provenance-utils/instance-input-file.txt
## data1_file: /tmp/test-file-provenance-utils/data1-file.txt
## data2_file: /tmp/test-file-provenance-utils/data2-file.txt
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

## To-Do/Coming Next

Please view the listing of planned improvements [here](docs/TODO.md).

## CHANGELOG

Please view the CHANGELOG [here](docs/CHANGELOG.md).

## License

[No License](docs/LICENSE)
