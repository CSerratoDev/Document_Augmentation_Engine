import os
import psycopg2
from psycopg2.extras import RealDictCursor

class UserConnection:
    def __init__(self):
        try:
            # Usamos variables de entorno para mayor flexibilidad
            self.conn = psycopg2.connect(
                dbname=os.getenv("POSTGRES_DB", "fastapi_db"),
                user=os.getenv("POSTGRES_USER", "fastapi_user"),
                password=os.getenv("POSTGRES_PASSWORD", "123456789"),
                host=os.getenv("POSTGRES_HOST", "db"),
                port=os.getenv("POSTGRES_PORT", "5432")
            )
        except psycopg2.OperationalError as err:
            print(f"Error al conectar a la base de datos: {err}")
            self.conn = None

    def write_user(self, data):
        """Inserta un nuevo usuario con los campos de tu esquema"""
        if not self.conn: return
        with self.conn.cursor() as cur:
            cur.execute("""
                INSERT INTO "user"(name, email, password, role) 
                VALUES(%(name)s, %(email)s, %(password)s, %(role)s)
            """, data)
        self.conn.commit()

    def write_document(self, data):
        """Inserta documentos según la nueva tabla documents"""
        if not self.conn: return
        with self.conn.cursor() as cur:
            cur.execute("""
                INSERT INTO "documents"(file_name, file_extension, company_id, file_url) 
                VALUES(%(file_name)s, %(file_extension)s, %(company_id)s, %(file_url)s)
            """, data)
        self.conn.commit()

    def get_company_data(self, company_id):
        """Ejemplo de consulta para obtener datos de compañía"""
        if not self.conn: return
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                SELECT c.name as company_name, d.file_name, d.file_url
                FROM "company" c
                JOIN "documents" d ON c.id = d.company_id
                WHERE c.id = %s
            """, (company_id,))
            return cur.fetchall()

    def close(self):
        if self.conn:
            self.conn.close()

    def __del__(self):
        self.close()