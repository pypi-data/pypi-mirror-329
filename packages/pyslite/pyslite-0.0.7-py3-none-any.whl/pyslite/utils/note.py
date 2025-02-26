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
    

    def show(self):
      try:
        from IPython import display, get_ipython
        get_ipython()
        if self.content:
          display_content = f"#{self.title}\n" + self.content
          display.display(display.Markdown(display_content))
        
      except:
        print(self.title)
        print(self.content)