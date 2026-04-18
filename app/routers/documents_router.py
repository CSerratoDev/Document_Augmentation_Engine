import os
import shutil
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from app.crud.documents_crud import create_document, get_all_documents, get_document, update_document, delete_document
from app.schemas.user_schema import DocumentSchema, DocumentResponse

router = APIRouter(
    prefix="/api/documents",
    tags=["Documents"]
)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

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

@router.post("/", response_model=DocumentResponse)
async def upload_document(
    company_id: int = Form(...),
    file: UploadFile = File(...)
):
    # 1. Validar extensión
    file_extension = file.filename.split('.')[-1].lower()
    if file_extension != "pdf":
        raise HTTPException(status_code=400, detail="Solo se permiten archivos PDF")

    # 2. Definir ruta y guardar archivo físicamente
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al guardar archivo: {str(e)}")

    # 3. Preparar datos para el CRUD
    document_data = {
        "file_name": file.filename,
        "file_extension": file_extension,
        # Guardamos solo el nombre para evitar conflictos con el mount
        # O guardamos la URL final que el frontend usará
        "file_url": f"uploads/{file.filename}", 
        "company_id": company_id
    }
    # 4. Registrar en la base de datos
    return create_document(document_data)

@router.get("/{document_id}", response_model=DocumentResponse)
async def read_document(document_id: int):
    return get_document(document_id)

@router.put("/{document_id}", response_model=DocumentResponse)
async def update_document_data(document_id: int, document_data: DocumentSchema):
    return update_document(document_id, document_data)

@router.delete("/{document_id}")
async def remove_document(document_id: int):
    return delete_document(document_id)