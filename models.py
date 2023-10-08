from pydantic import BaseModel, Field
from typing import Optional

class NGOPydanticModel(BaseModel):
    id: Optional[int] = Field(default=None)
    name: Optional[str] = Field(default = None)
    miasto: Optional[str] = Field(default = None)
    street: Optional[str] = Field(default = None)
    krs: Optional[str] = Field(default = None)
    phone: Optional[str] = Field(default = None)
    op: Optional[str] = Field(default = None) 
    status: Optional[str] = Field(default = None)
    dzial: Optional[str] = Field(default = None)
    numer: Optional[str] = Field(default = None)

class NGOUserPydanticModel(BaseModel):
    id: Optional[int] = Field(default=None, primary_key=True)
    login: str  
    password: str