import aiosqlite # type: ignore
from typing import Dict, Any, List, Optional
from pathlib import Path
from .base import BaseDriver

class SQLiteDriver(BaseDriver):
    def __init__(self):
        self.db_path = None
        self.connection = None

    async def connect(self, dsn: str) -> None:
        """Conecta a la base de datos SQLite"""
        # El DSN para SQLite será del tipo: sqlite:///path/to/db.sqlite
        self.db_path = dsn.replace('sqlite:///', '')
        
        # Asegurar que el directorio existe
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
        
        self.connection = await aiosqlite.connect(self.db_path)
        self.connection.row_factory = aiosqlite.Row

    async def close(self) -> None:
        """Cierra la conexión"""
        if self.connection:
            await self.connection.close()

    async def fetch(self, query: str, *args) -> List[Dict[str, Any]]:
        """Ejecuta una query y retorna múltiples resultados"""
        async with self.connection.execute(query, args) as cursor:
            rows = await cursor.fetchall()
            return [dict(row) for row in rows]

    async def fetch_one(self, query: str, *args) -> Optional[Dict[str, Any]]:
        """Ejecuta una query y retorna un único resultado"""
        async with self.connection.execute(query, args) as cursor:
            row = await cursor.fetchone()
            return dict(row) if row else None

    async def execute(self, query: str, *args) -> None:
        """Ejecuta una query sin retornar resultados"""
        async with self.connection.execute(query, args):
            await self.connection.commit()

    async def _introspect_sqlite(self) -> Dict[str, Any]:
        """Obtiene información del esquema de la base de datos"""
        tables_query = """
        SELECT 
            name as table_name
        FROM sqlite_master 
        WHERE type='table' AND name NOT LIKE 'sqlite_%'
        """
        
        schema_info = {}
        tables = await self.fetch(tables_query)
        
        for table in tables:
            table_name = table['table_name']
            columns_query = f"PRAGMA table_info('{table_name}')"
            columns = await self.fetch(columns_query)
            
            schema_info[table_name] = {
                'fields': {
                    col['name']: {
                        'type': col['type'].lower(),
                        'nullable': not col['notnull'],
                        'default': col['dflt_value'],
                        'primary': bool(col['pk'])
                    }
                    for col in columns
                }
            }
        
        return schema_info 