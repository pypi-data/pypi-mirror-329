import json
from dataclasses import dataclass, asdict
from typing import Optional


@dataclass
class Tile:
  title: str = ""
  iconURL: str = None
  colorHex: str = None
  label: str = None
  url: str = None
  content: str = None

  def __post_init__(self):
    if self.colorHex and not self.label:
      raise ValueError("Can not have status without label.")


  def json(self):
    clean_dict = {}
    status = {}
    for key,value in asdict(self).items():
      if value:
        if key in ["label", "colorHex"]:
          status[key] = value
        else:
          clean_dict[key] = value
    if status:
      clean_dict["status"] = status
    return json.dumps(asdict(self))