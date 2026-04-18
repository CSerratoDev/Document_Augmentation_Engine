from fastapi import HTTPException
from app.database.db import get_connection
from app.schemas.user_schema import DocumentSchema, DocumentResponse

def create_document(document_data: dict):
    conn = None
    try:
        conn = get_connection()
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO documents (file_name, file_extension, file_url, company_id)
                VALUES (%(file_name)s, %(file_extension)s, %(file_url)s, %(company_id)s)
                RETURNING id, file_name, file_extension, file_url, company_id, uploaded_at;
            """, document_data)
            row = cur.fetchone()
            conn.commit()
            return {
                "id": row[0],
                "file_name": row[1],
                "file_extension": row[2],
                "file_url": row[3],
                "company_id": row[4],
                "uploaded_at": str(row[5])
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if conn: conn.close()

def get_all_documents(
    skip: int = 0,
    limit: int = 10,
    extension: str | None = None,
    company_id: int | None = None,
):
    conn = None
    try:
        conn = get_connection()
        with conn.cursor() as cur:
            query = "SELECT id, file_name, file_extension, file_url, company_id, uploaded_at FROM documents"
            filters = []
            params = []

            if extension:
                filters.append("file_extension = %s")
                params.append(extension)
            if company_id:
                filters.append("company_id = %s")
                params.append(company_id)

            if filters:
                query += " WHERE " + " AND ".join(filters)

            query += " ORDER BY id DESC LIMIT %s OFFSET %s"
            params.extend([limit, skip])

            cur.execute(query, params)
            rows = cur.fetchall()

            if not rows:
                return []
            
            return [
                DocumentResponse(
                    id=row[0],
                    file_name=row[1],
                    file_extension=row[2],
                    file_url=row[3],
                    company_id=row[4],
                    uploaded_at=str(row[5])
                ) for row in rows
            ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if conn:
            conn.close()

def get_document(document_id: int):
    conn = None
    try:
        conn = get_connection()
        with conn.cursor() as cur:
            cur.execute("SELECT id, file_name, file_extension, file_url, company_id, uploaded_at FROM documents WHERE id = %s", (document_id,))
            row = cur.fetchone()
            if not row:
                raise HTTPException(status_code=404, detail=f"Document {document_id} not found")
            return {
                "id": row[0],
                "file_name": row[1],
                "file_extension": row[2],
                "file_url": row[3],
                "company_id": row[4],
                "uploaded_at": str(row[5])
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if conn:
            conn.close()

def update_document(document_id: int, document_data: DocumentSchema):
    conn = None
    try:
        conn = get_connection()
        with conn.cursor() as cur:
            cur.execute("""
                UPDATE documents
                SET file_name = %s, file_extension = %s, file_url = %s, company_id = %s
                WHERE id = %s
                RETURNING id, file_name, file_extension, file_url, company_id, uploaded_at;
            """, (document_data.file_name, document_data.file_extension, document_data.file_url, document_data.company_id, document_id))
            row = cur.fetchone()
            if not row:
                raise HTTPException(status_code=404, detail=f"Document {document_id} not found")
            conn.commit()
            return DocumentResponse(
                id=row[0], file_name=row[1], file_extension=row[2], file_url=row[3], company_id=row[4], uploaded_at=str(row[5])
            )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if conn:
            conn.close()

def delete_document(document_id: int):
    conn = None
    try:
        conn = get_connection()
        with conn.cursor() as cur:
            cur.execute("DELETE FROM documents WHERE id = %s RETURNING id;", (document_id,))
            if not cur.fetchone():
                raise HTTPException(status_code=404, detail=f"Document {document_id} not found")
            conn.commit()
        return {"message": f"Document {document_id} deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if conn:
            conn.close()