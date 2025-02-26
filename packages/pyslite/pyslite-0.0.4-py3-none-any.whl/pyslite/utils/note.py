from datetime import datetime
from typing import List
from pydantic import BaseModel, validator
from typing import Optional

from enum import Enum

class ReviewState(Enum):
  Verified = "Verified"
  Outdated = "Outdated"
  VerificationRequested = "VerificationRequested"


class Note(BaseModel):
    updatedAt: datetime
    url: str
    parentNoteId: str
    title: str
    id: str
    content: Optional[str] = None  # content can be missing
    reviewState: Optional[ReviewState] = None
    columns: Optional[List[str]] = None
    attributes: Optional[List[str]] = None
    
    @validator("updatedAt")
    def parse_datetime(cls, value):
        return datetime.fromisoformat(value.replace('Z', '+00:00'))


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