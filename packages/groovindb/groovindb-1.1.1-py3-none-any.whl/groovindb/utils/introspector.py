from typing import List, Dict, Any
from ..utils.logger import logger

class DatabaseIntrospector:
    def __init__(self, driver):
        self.driver = driver

    async def get_all_schemas(self) -> List[str]:
        """Obtiene todos los schemas disponibles"""
        try:
            if hasattr(self.driver, '_introspect_postgresql'):
                query = """
                SELECT nspname as schema_name 
                FROM pg_namespace 
                WHERE nspname NOT IN ('information_schema', 'pg_catalog', 'pg_toast')
                    AND nspname NOT LIKE 'pg_%'
                ORDER BY nspname;
                """
                schemas = await self.driver.fetch(query)
                return [schema['schema_name'] for schema in schemas]
                
            elif hasattr(self.driver, '_introspect_mysql'):
                query = """
                SELECT SCHEMA_NAME as schema_name
                FROM INFORMATION_SCHEMA.SCHEMATA
                WHERE SCHEMA_NAME NOT IN 
                    ('information_schema', 'mysql', 'performance_schema', 'sys')
                """
                schemas = await self.driver.fetch(query)
                return [schema['schema_name'] for schema in schemas]
                
            else:  # SQLite
                return ['public']
                
        except Exception as e:
            logger.error(f"Error obteniendo schemas: {e}")
            return ['public']  # Fallback a public si hay error

    async def get_schema_info(self, schema: str) -> Dict[str, Any]:
        """Obtiene información de un schema específico"""
        try:
            if hasattr(self.driver, '_introspect_postgresql'):
                return await self.driver._introspect_postgresql(schema)
            elif hasattr(self.driver, '_introspect_mysql'):
                return await self.driver._introspect_mysql(schema)
            elif hasattr(self.driver, '_introspect_sqlite'):
                return await self.driver._introspect_sqlite()
            else:
                logger.error(f"Driver no soportado para introspección")
                return {}
        except Exception as e:
            logger.error(f"Error obteniendo información del schema {schema}: {str(e)}")
            return {}

    async def get_all_schemas_info(self) -> Dict[str, Dict[str, Any]]:
        """Obtiene la información de todos los schemas"""
        schemas = await self.get_all_schemas()
        logger.info(f"Schemas encontrados: {schemas}")
        
        schema_info = {}
        for schema in schemas:
            try:
                info = await self.get_schema_info(schema)
                if info:  # Solo agregar si se obtuvo información
                    schema_info[schema] = info
                    logger.debug(f"Schema {schema}: {len(info)} tablas encontradas")
            except Exception as e:
                logger.error(f"Error procesando schema {schema}: {e}")
                continue
            
        return schema_info 