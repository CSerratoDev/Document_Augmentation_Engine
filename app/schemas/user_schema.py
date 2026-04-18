from pydantic import BaseModel, EmailStr
from typing import Literal, Optional

#Ready
class UserSchema(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: Literal["client", "seller"]
#Ready
class UserResponse(BaseModel):
    id: int | None = None
    name: str
    email: EmailStr
    role: Literal["client", "seller"]
#Ready
class DocumentSchema(BaseModel):
    file_name: str
    file_extension: Literal["pdf", "txt"]
    file_url: Optional[str] = None
    company_id: int

class DocumentResponse(DocumentSchema):
    id: int
    uploaded_at: Optional[str] = None

class Company(BaseModel):
    id: int
    name: str
    agent: list[UserResponse] | None = None
    documents: list[DocumentResponse] | None = None
    img_url: Optional[str] = None

    @property
    def total_documents(self) -> int:
        return len(self.documents) if self.documents else 0