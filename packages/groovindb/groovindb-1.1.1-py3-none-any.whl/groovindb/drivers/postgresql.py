from typing import Dict, Any, List, Optional
import asyncpg
from .base import BaseDriver
from ..utils.logger import logger


class PostgreSQLDriver(BaseDriver):
    async def rollback(self) -> None:
        pass

    async def commit(self) -> None:
        pass

    async def begin(self) -> None:
        pass

    def __init__(self):
        self.conn = None

    async def connect(self, dsn: str) -> None:
        self.conn = await asyncpg.connect(dsn)

    async def close(self) -> None:
        if self.conn:
            await self.conn.close()

    async def fetch(self, query: str, *args) -> List[Dict[str, Any]]:
        records = await self.conn.fetch(query, *args)
        return [dict(r) for r in records]

    async def fetch_one(self, query: str, *args) -> Optional[Dict[str, Any]]:
        record = await self.conn.fetchrow(query, *args)
        return dict(record) if record else None

    async def execute(self, query: str, *args) -> None:
        """Ejecuta una query sin retornar resultados"""
        await self.conn.execute(query, *args) 

    async def _introspect_postgresql(self, schema: str) -> Dict[str, Any]:
        """Introspección específica para PostgreSQL"""
        try:
            query = """
            SELECT 
                t.table_name,
                c.column_name,
                c.data_type,
                c.is_nullable = 'YES' as is_nullable,
                c.column_default,
                c.character_maximum_length,
                c.numeric_precision,
                c.numeric_scale,
                (
                    SELECT EXISTS (
                        SELECT 1 
                        FROM information_schema.table_constraints tc
                        JOIN information_schema.constraint_column_usage ccu 
                        ON tc.constraint_name = ccu.constraint_name
                        WHERE tc.table_schema = t.table_schema
                        AND tc.table_name = t.table_name
                        AND tc.constraint_type = 'PRIMARY KEY'
                        AND ccu.column_name = c.column_name
                    )
                ) as is_primary
            FROM information_schema.tables t
            JOIN information_schema.columns c 
                ON t.table_schema = c.table_schema 
                AND t.table_name = c.table_name
            WHERE t.table_schema = $1
                AND t.table_type = 'BASE TABLE'
            ORDER BY t.table_name, c.ordinal_position
            """
            
            columns = await self.fetch(query, schema)
            
            # Organizar la información por tablas
            schema_info = {}
            for col in columns:
                table_name = col['table_name']
                if table_name not in schema_info:
                    schema_info[table_name] = {'fields': {}}
                    
                schema_info[table_name]['fields'][col['column_name']] = {
                    'type': col['data_type'],
                    'nullable': col['is_nullable'],
                    'default': col['column_default'],
                    'primary': col['is_primary'],
                    'length': col['character_maximum_length'],
                    'precision': col['numeric_precision'],
                    'scale': col['numeric_scale']
                }
            
            return schema_info
        except Exception as e:
            logger.error(f"Error en introspección PostgreSQL: {str(e)}")
            return {}

