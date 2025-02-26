import dataclasses
from datetime import datetime
import json
from dataclasses import dataclass, field
from typing import List

from typing import Optional

from enum import Enum

class ReviewState(Enum):
  Verified = "Verified"
  Outdated = "Outdated"
  VerificationRequested = "VerificationRequested"

@dataclass
class Note:
  updatedAt: datetime
  columns: Optional[List]
  attributes: Optional[List]
  url: str
  parentNoteId: str
  title: str
  id: str
  content: str
  reviewState: Optional[ReviewState] = None


  def __post_init__(self):
    if self.columns and self.attributes:
      print("ITS A COLLECTION")
      self.collection = True


  def show(self):
    try:
      from IPython import display, get_ipython
      get_ipython()
      if self.content:
        content = f"#{self.title}\n" + self.content
        display.display(display.Markdown(content))
      else:
        return "No Content"
    except:
      print(self.title)
      print(self.content)


  def json(self):
    clean_dict = {}
    for key,value in dataclasses.asdict(self).items():
      if value:
        clean_dict[key] = value
    return json.dumps(dataclasses.asdict(self))