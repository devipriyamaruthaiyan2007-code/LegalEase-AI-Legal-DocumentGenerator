from pydantic import BaseModel, Field

class DocumentRequest(BaseModel):
    document_type: str = Field(..., min_length=2)
    parties: str = Field(..., min_length=2)
    terms: str = Field(..., min_length=2)
    effective_date: str = Field(..., min_length=2)
