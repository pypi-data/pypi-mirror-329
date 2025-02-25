# Insider Scripts

## Purpose

Run python scripts from inside a package without relative import error.

## Installation

```
pip install insider_scripts
```

## Usage

Import the function define script from the insider_scripts and call it with either the depth of the script in the package, or the path of the package root.

### Example layout

```
your_package/
|-- A_folder/
|   ├── A.py
|   └── script.py
|-- B_folder/
|   └── B.py
```

### Example script:\n"

```python
from pathlib import Path
from insider_scripts import define_script
define_script(1) # or define_script(Path(__file__).parent.parent) or define_script(-1)

from .A import A
from ..B_folder.B import B
```