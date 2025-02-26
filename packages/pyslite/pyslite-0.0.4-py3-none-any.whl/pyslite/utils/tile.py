from typing import Optional
from pydantic import BaseModel, validator



class Tile(BaseModel):
    title: str = ""
    iconURL: Optional[str] = None
    colorHex: Optional[str] = None
    label: Optional[str] = None
    url: Optional[str] = None
    content: Optional[str] = None

    @validator("*")
    def check_status(cls, v, field):
        if field.name == "colorHex" and v and not cls.__fields__.get("label"):
            raise ValueError("Can not have colorHex without label.")
        return v