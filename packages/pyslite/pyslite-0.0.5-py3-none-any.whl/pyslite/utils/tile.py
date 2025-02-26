from typing import Optional
from pydantic import BaseModel, validator


class Tile(BaseModel):
    title: str = ""
    iconURL: Optional[str] = None
    colorHex: Optional[str] = None
    label: Optional[str] = None
    url: Optional[str] = None
    content: Optional[str] = None

    @validator("colorHex")
    def check_colorhex_and_label(cls, v):
        if v and not cls.label:  # Access label directly from the class
            raise ValueError("colorHex cannot be set without label.")
        return v

