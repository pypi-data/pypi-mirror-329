from datetime import datetime
from typing import List, Optional
from enum import Enum
from pydantic import BaseModel


class ReviewState(str, Enum):
    Verified = "Verified"
    Outdated = "Outdated"
    VerificationRequested = "VerificationRequested"


class Note(BaseModel):
    updatedAt: datetime
    url: str
    parentNoteId: str
    title: str
    id: str
    content: Optional[str] = ""  # content can be missing
    reviewState: Optional[ReviewState] = None
    columns: Optional[List[str]] = None
    attributes: Optional[List[str]] = None


    def show(self):
        try:
            from IPython import display, get_ipython
            get_ipython()  # Check if running in IPython
            if self.content:
                content = f"# {self.title}\n" + self.content
                display.display(display.Markdown(content))
            else:
                return "No Content"
        except ImportError:
            print(f"Note Title: {self.title}")
            if self.content:
                print(f"Note Content:\n{self.content}")
            else:
                print("No Content")
        except Exception as e:
            print(f"An error occurred: {e}")

