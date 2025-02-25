from typing import Dict, Any, List, Optional
import aiomysql
from urllib.parse import urlparse
from .base import BaseDriver

class MySQLDriver(BaseDriver):
    def __init__(self):
        self.pool = None

    async def connect(self, dsn: str) -> None:
        url = urlparse(dsn)
        self.pool = await aiomysql.create_pool(
            host=url.hostname,
            port=url.port or 3306,
            user=url.username,
            password=url.password,
            db=url.path[1:],
            autocommit=True
        )

    async def close(self) -> None:
        if self.pool:
            self.pool.close()
            await self.pool.wait_closed()

    async def fetch(self, query: str, *args) -> List[Dict[str, Any]]:
        async with self.pool.acquire() as conn:
            async with conn.cursor(aiomysql.DictCursor) as cur:
                await cur.execute(query, args)
                return await cur.fetchall()

    async def fetch_one(self, query: str, *args) -> Optional[Dict[str, Any]]:
        async with self.pool.acquire() as conn:
            async with conn.cursor(aiomysql.DictCursor) as cur:
                await cur.execute(query, args)
                result = await cur.fetchone()
                return dict(result) if result else None

    async def execute(self, query: str, *args) -> None:
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(query, args)
                await conn.commit()

    async def _introspect_mysql(self, schema: str) -> Dict[str, Any]:
        """Introspección específica para MySQL"""
        query = """
        SELECT 
            TABLE_NAME as table_name,
            COLUMN_NAME as column_name,
            DATA_TYPE as data_type,
            IS_NULLABLE = 'YES' as is_nullable,
            COLUMN_DEFAULT as column_default,
            CHARACTER_MAXIMUM_LENGTH as char_length,
            NUMERIC_PRECISION as num_precision,
            NUMERIC_SCALE as num_scale,
            COLUMN_KEY = 'PRI' as is_primary
        FROM INFORMATION_SCHEMA.COLUMNS
        WHERE TABLE_SCHEMA = %s
        ORDER BY TABLE_NAME, ORDINAL_POSITION
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
                'length': col['char_length'],
                'precision': col['num_precision'],
                'scale': col['num_scale']
            }
        
        return schema_info 