from fastapi import APIRouter, HTTPException
from backend.models import DocumentRequest
from ai_core.generator import LegalDocumentGenerator

router = APIRouter()
generator = LegalDocumentGenerator()

@router.post("/generate")
def generate_document(request: DocumentRequest):
    try:
        document = generator.generate_document(
            document_type=request.document_type,
            parties=request.parties,
            terms=request.terms,
            effective_date=request.effective_date,
        )
        return {"success": True, "document": document}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
