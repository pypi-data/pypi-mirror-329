import os
import sys
from pathlib import Path
from importlib.machinery import ModuleSpec
import __main__

def define_script(depth_or_root: int | str | Path=0):
  file_path = Path(getattr(__main__, "__file__", os.getcwd() + "/main.py"))
  if __main__.__spec__ is not None: return
  if isinstance(depth_or_root, int):
    root_path = file_path.parents[abs(depth_or_root)]
  elif isinstance(depth_or_root, str):
    root_path = Path(depth_or_root).resolve()
  elif isinstance(depth_or_root, Path):
    root_path = depth_or_root.resolve()
  else:
    raise ValueError(f"depth_or_root must be int, str or Path, not {type(depth_or_root)}.")

  module_name = str(file_path.relative_to(root_path.parent, walk_up=True).with_suffix("").as_posix()).replace("/", ".")
  if str(root_path.parent) not in sys.path:
    sys.path.insert(0, str(root_path.parent))
  __main__.__spec__ = ModuleSpec(name=module_name, loader=None)