from fastapi import APIRouter
from app.crud.documents_crud import create_document, get_all_documents, get_document, update_document, delete_document
from app.schemas.user_schema import DocumentSchema, DocumentResponse

router = APIRouter(
    prefix="/api/documents",
    tags=["Documents"]
)

@router.get("/", response_model=list[DocumentResponse])
async def read_documents(
    page: int = 1,
    limit: int = 10,
    extension: str | None = None,
    company_id: int | None = None
):
    skip = (page - 1) * limit
    return get_all_documents(
        skip=skip,
        limit=limit,
        extension=extension,
        company_id=company_id
    )

@router.post("/")
async def write_document(document_data: DocumentSchema):
    return create_document(document_data.model_dump())

@router.get("/{document_id}", response_model=DocumentResponse)
async def read_document(document_id: int):
    return get_document(document_id)

@router.put("/{document_id}", response_model=DocumentResponse)
async def update_document_data(document_id: int, document_data: DocumentSchema):
    return update_document(document_id, document_data)

@router.delete("/{document_id}")
async def remove_document(document_id: int):
    return delete_document(document_id)