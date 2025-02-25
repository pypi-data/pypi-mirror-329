from typing import Dict, Any, Optional, List, TypeVar, Generic, Union
from ..types import WhereInput, OrderByInput, SelectInput
from ..utils.validator import (
    validate_input, OPERATORS, SortOrder,
    ValidationError
)
from ..utils.logger import logger
import json

T = TypeVar('T')

class Table(Generic[T]):
    def __init__(self, db: 'GroovinDB', database: str, schema: str, table: str):
        self._db = db
        self._database = database
        self._schema = schema
        self._table = table
        self._column_types = {}
        self._initialized = False

    async def _ensure_initialized(self):
        """Asegura que los tipos de columnas estén cargados"""
        if not self._initialized:
            await self._load_column_types()
            self._initialized = True

    async def _load_column_types(self):
        """Carga los tipos de columnas de la base de datos"""
        driver = self._db._drivers[self._database]
        
        if hasattr(driver, '_introspect_postgresql'):
            query = """
                SELECT column_name, data_type, udt_name
                FROM information_schema.columns
                WHERE table_schema = $1 AND table_name = $2
            """
            columns = await driver.fetch(query, self._schema, self._table)
            for col in columns:
                self._column_types[col['column_name']] = col['udt_name']
        else:
            # MySQL
            query = """
                SELECT column_name, data_type
                FROM information_schema.columns
                WHERE table_schema = %s AND table_name = %s
            """
            columns = await driver.fetch(query, self._schema, self._table)
            for col in columns:
                self._column_types[col['column_name']] = col['data_type']

    def _convert_value(self, column: str, value: Any) -> Any:
        """Convierte el valor al tipo correcto según la columna"""
        if value is None:
            return None
            
        column_type = self._column_types.get(column, '').lower()
        
        try:
            if column_type in ('int4', 'int8', 'integer', 'bigint'):
                return int(value)
            elif column_type in ('float4', 'float8', 'real', 'double precision'):
                return float(value)
            elif column_type in ('bool', 'boolean'):
                return bool(value)
            elif column_type in ('json', 'jsonb'):
                return value if isinstance(value, (dict, list)) else json.loads(value)
            else:
                return value
        except (ValueError, TypeError) as e:
            raise ValidationError(f"Error convirtiendo valor '{value}' para la columna '{column}' de tipo {column_type}: {str(e)}")

    def _build_where(self, where: WhereInput) -> tuple[str, list]:
        """Construye la cláusula WHERE y retorna también los parámetros"""
        conditions = []
        params = []
        param_count = 1
        
        for field, condition in where.items():
            if isinstance(condition, dict):
                for op, value in condition.items():
                    cond, param = self._build_condition(field, op, value)
                    if hasattr(self._db._drivers[self._database], '_introspect_postgresql'):
                        cond = cond.replace('$', f'${param_count}')
                        param_count += len(param) if isinstance(param, (list, tuple)) else 1
                    conditions.append(cond)
                    if param is not None:
                        # Convertir cada valor al tipo correcto
                        if isinstance(param, (list, tuple)):
                            param = [self._convert_value(field, v) for v in param]
                        else:
                            param = self._convert_value(field, param)
                        params.extend(param if isinstance(param, (list, tuple)) else [param])
            else:
                if hasattr(self._db._drivers[self._database], '_introspect_postgresql'):
                    cond = f"{field} = ${param_count}"
                    param_count += 1
                else:
                    cond = f"{field} = %s"
                conditions.append(cond)
                # Convertir el valor al tipo correcto
                params.append(self._convert_value(field, condition))
                    
        return " AND ".join(conditions), params

    async def findFirst(self, 
        where: Optional[WhereInput] = None,
        order_by: Optional[OrderByInput] = None,
        select: Optional[SelectInput] = None
    ) -> Optional[T]:
        """Encuentra el primer registro que coincida con los criterios"""
        try:
            await self._db._ensure_connected(self._database)
            driver = self._db._drivers[self._database]
            
            # Validar inputs
            validate_input(where=where, order_by=order_by, select=select)
            
            # Construir query
            table_name = self._get_table_name()
            query_parts = [f"SELECT {self._build_select(select)} FROM {table_name}"]
            params: List[Any] = []
            
            if where:
                where_clause, where_params = self._build_where(where)
                query_parts.append(f"WHERE {where_clause}")
                params.extend(where_params)
            
            if order_by:
                order_clause = self._build_order_by(order_by)
                query_parts.append(order_clause)
            
            query_parts.append("LIMIT 1")
            query = " ".join(query_parts)
            
            logger.debug(f"Query: {query}, Params: {params}")
            return await driver.fetch_one(query, *params)
            
        except Exception as e:
            logger.error(f"Error en findFirst: {str(e)}")
            raise

    async def findMany(self,
        where: Optional[WhereInput] = None,
        order_by: Optional[OrderByInput] = None,
        select: Optional[SelectInput] = None,
        take: Optional[int] = None,
        skip: Optional[int] = None
    ) -> List[T]:
        """Encuentra múltiples registros que coincidan con los criterios"""
        try:
            await self._db._ensure_connected(self._database)
            await self._ensure_initialized()  # Asegurarse de que los tipos estén cargados
            
            driver = self._db._drivers[self._database]
            
            validate_input(
                where=where,
                order_by=order_by,
                select=select,
                take=take,
                skip=skip
            )
            
            # Construir query
            table_name = self._get_table_name()
            query_parts = [f"SELECT {self._build_select(select)} FROM {table_name}"]
            params: List[Any] = []
            
            if where:
                where_clause, where_params = self._build_where(where)
                query_parts.append(f"WHERE {where_clause}")
                params.extend(where_params)
            
            if order_by:
                order_clause = self._build_order_by(order_by)
                query_parts.append(order_clause)
            
            if skip:
                query_parts.append(f"OFFSET {skip}")
            
            if take:
                query_parts.append(f"LIMIT {take}")
            
            query = " ".join(query_parts)
            
            logger.debug(f"Query: {query}, Params: {params}")
            return await driver.fetch(query, *params)
            
        except Exception as e:
            logger.error(f"Error en findMany: {str(e)}")
            raise

    def _build_select(self, select: Optional[SelectInput] = None) -> str:
        """Construye la parte SELECT de la query"""
        if not select:
            return "*"
        fields = [field for field, include in select.items() if include]
        return ", ".join(fields) if fields else "*"

    def _build_condition(self, field: str, operator: str, value: Any) -> tuple[str, Optional[Any]]:
        """Construye una condición individual y retorna la condición y su parámetro"""
        if operator not in OPERATORS:
            raise ValidationError(f"Operador no soportado: {operator}")
            
        # Determinar el estilo de placeholder según el driver
        placeholder = "$" if hasattr(self._db._drivers[self._database], '_introspect_postgresql') else "%s"
        
        if operator in ["isNull", "isNotNull"]:
            return f"{field} {OPERATORS[operator]}", None
            
        if operator == "contains":
            return f"{field} LIKE {placeholder}", f"%{value}%"
        elif operator == "startsWith":
            return f"{field} LIKE {placeholder}", f"{value}%"
        elif operator == "endsWith":
            return f"{field} LIKE {placeholder}", f"%{value}"
        elif operator in ["in", "notIn"]:
            placeholders = []
            for i in range(len(value)):
                if hasattr(self._db._drivers[self._database], '_introspect_postgresql'):
                    placeholders.append(f"${i+1}")
                else:
                    placeholders.append("%s")
            return f"{field} {OPERATORS[operator]} ({','.join(placeholders)})", value
        elif operator in ["between", "notBetween"]:
            if hasattr(self._db._drivers[self._database], '_introspect_postgresql'):
                return f"{field} {OPERATORS[operator]} $1 AND $2", value
            else:
                return f"{field} {OPERATORS[operator]} %s AND %s", value
        else:
            return f"{field} {OPERATORS[operator]} {placeholder}", value

    def _build_order_by(self, order_by: OrderByInput) -> str:
        """Construye la cláusula ORDER BY"""
        orders = []
        for field, direction in order_by.items():
            direction = direction.upper()
            if direction not in [SortOrder.ASC.upper(), SortOrder.DESC.upper()]:
                raise ValidationError(f"Dirección de ordenamiento inválida: {direction}")
            orders.append(f"{field} {direction}")
        return "ORDER BY " + ", ".join(orders)

    def _get_table_name(self) -> str:
        """Retorna el nombre de la tabla con el formato correcto según el driver"""
        driver = self._db._drivers[self._database]
        if hasattr(driver, '_introspect_postgresql'):
            return f'"{self._schema}"."{self._table}"'
        elif hasattr(driver, '_introspect_mysql'):
            return f"`{self._schema}`.`{self._table}`"
        else:  # SQLite
            return f'"{self._table}"'

    def _format_field(self, field: str) -> str:
        """Formatea el nombre del campo según el driver"""
        driver = self._db._drivers[self._database]
        if hasattr(driver, '_introspect_postgresql'):
            return f'"{field}"'
        elif hasattr(driver, '_introspect_mysql'):
            return f"`{field}`"
        else:
            return f'"{field}"'

    def _get_placeholder(self, is_postgres: bool, param_count: int) -> str:
        """Helper para obtener el placeholder correcto según el driver"""
        return f"${param_count}" if is_postgres else "%s"

    async def findUnique(self, where: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Encuentra un registro único"""
        try:
            validate_input(where=where)
        except ValidationError as e:
            logger.error(f"Error de validación en findUnique: {e}")
            raise

        if hasattr(self._db.driver, '_introspect_mysql'):
            conditions = [f"`{k}` = %s" for k in where.keys()]
            query = f"SELECT * FROM `{self._schema}`.`{self._table}` WHERE {' AND '.join(conditions)} LIMIT 1"
        else:
            conditions = [f'"{k}" = ${i+1}' for i, k in enumerate(where.keys())]
            query = f'SELECT * FROM "{self._schema}"."{self._table}" WHERE {" AND ".join(conditions)} LIMIT 1'

        return await self._db.driver.fetch_one(query, *where.values())

    async def create(self, data):
        """Crea un nuevo registro"""
        await self._db._ensure_connected(self._database)
        driver = self._db._drivers[self._database]
        is_postgres = driver.__class__.__name__ == 'PostgreSQLDriver'
        param_count = 1

        fields = []
        values = []
        placeholders = []
        params = []

        for field, value in data.items():
            fields.append(self._format_field(field))
            placeholder = self._get_placeholder(is_postgres, param_count)
            placeholders.append(placeholder)
            params.append(value)
            param_count += 1

        query = f"INSERT INTO {self._schema}.{self._table} ({', '.join(fields)}) VALUES ({', '.join(placeholders)}) RETURNING *"
        result = await driver.fetch(query, *params)
        return result[0] if result else None

    async def update(self, where, data):
        """Actualiza registros que coincidan con los criterios"""
        await self._db._ensure_connected(self._database)
        driver = self._db._drivers[self._database]
        is_postgres = driver.__class__.__name__ == 'PostgreSQLDriver'
        param_count = 1

        # SET
        set_clauses = []
        params = []
        for field, value in data.items():
            placeholder = self._get_placeholder(is_postgres, param_count)
            set_clauses.append(f"{self._format_field(field)} = {placeholder}")
            params.append(value)
            param_count += 1

        # WHERE
        where_clauses = []
        for field, value in where.items():
            placeholder = self._get_placeholder(is_postgres, param_count)
            where_clauses.append(f"{self._format_field(field)} = {placeholder}")
            params.append(value)
            param_count += 1

        query = f"""
            UPDATE {self._schema}.{self._table} 
            SET {', '.join(set_clauses)}
            WHERE {' AND '.join(where_clauses)}
            RETURNING *
        """
        result = await driver.fetch(query, *params)
        return result[0] if result else None

    async def upsert(self,
        where: Dict[str, Any],
        create: Dict[str, Any],
        update: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Crea o actualiza un registro"""
        try:
            validate_input(where=where, create=create, update=update)
        except ValidationError as e:
            logger.error(f"Error de validación en upsert: {e}")
            raise

        existing = await self.findUnique(where)
        if existing:
            return await self.update(where, update)
        return await self.create(create)

    async def delete(self, where):
        """Elimina registros que coincidan con los criterios"""
        await self._db._ensure_connected(self._database)
        driver = self._db._drivers[self._database]
        is_postgres = driver.__class__.__name__ == 'PostgreSQLDriver'
        param_count = 1

        where_clauses = []
        params = []
        for field, value in where.items():
            placeholder = self._get_placeholder(is_postgres, param_count)
            where_clauses.append(f"{self._format_field(field)} = {placeholder}")
            params.append(value)
            param_count += 1

        query = f"""
            DELETE FROM {self._schema}.{self._table}
            WHERE {' AND '.join(where_clauses)}
            RETURNING *
        """
        result = await driver.fetch(query, *params)
        return result[0] if result else None

    async def count(self, where: Optional[Dict[str, Any]] = None) -> int:
        """Cuenta registros"""
        try:
            validate_input(where=where)
        except ValidationError as e:
            logger.error(f"Error de validación en count: {e}")
            raise

        query = f'SELECT COUNT(*) as count FROM "{self._schema}"."{self._table}"'
        params = []
        
        if where:
            conditions = []
            for field, value in where.items():
                conditions.append(f'"{field}" = ${len(params) + 1}')
                params.append(value)
            if conditions:
                query += " WHERE " + " AND ".join(conditions)
                
        result = await self._db.driver.fetch_one(query, *params)
        return result['count']

    async def aggregate(self,
        where: Optional[Dict[str, Any]] = None,
        _sum: Optional[List[str]] = None,
        _avg: Optional[List[str]] = None,
        _min: Optional[List[str]] = None,
        _max: Optional[List[str]] = None,
        _count: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """Realiza operaciones de agregación"""
        try:
            validate_input(where=where, aggregate={
                "_sum": _sum or [],
                "_avg": _avg or [],
                "_min": _min or [],
                "_max": _max or [],
                "_count": _count or []
            })
        except ValidationError as e:
            logger.error(f"Error de validación en aggregate: {e}")
            raise

        aggregations = []
        if _sum: aggregations.extend([f'SUM("{field}") as sum_{field}' for field in _sum])
        if _avg: aggregations.extend([f'AVG("{field}") as avg_{field}' for field in _avg])
        if _min: aggregations.extend([f'MIN("{field}") as min_{field}' for field in _min])
        if _max: aggregations.extend([f'MAX("{field}") as max_{field}' for field in _max])
        if _count: aggregations.extend([f'COUNT("{field}") as count_{field}' for field in _count])
        
        if not aggregations:
            aggregations = ["COUNT(*) as count"]
        
        query = f'SELECT {", ".join(aggregations)} FROM "{self._schema}"."{self._table}"'
        params = []

        if where:
            conditions = []
            for field, value in where.items():
                condition, new_params = self._build_where_condition(field, value, len(params))
                conditions.append(condition)
                params.extend(new_params)
            if conditions:
                query += " WHERE " + " AND ".join(conditions)

        return await self._db.driver.fetch_one(query, *params)

    async def createMany(self, 
        data: List[Dict[str, Any]],
        skipDuplicates: bool = False
    ) -> Dict[str, int]:
        """
        Inserta múltiples registros en la tabla.
        
        Args:
            data: Lista de diccionarios con los datos a insertar
            skipDuplicates: Si es True, ignora registros duplicados
        
        Returns:
            Dict con la cantidad de registros insertados
        """
        if not data:
            return {"count": 0}

        # Obtener las columnas del primer registro
        columns = list(data[0].keys())
        
        # Construir la query
        placeholders = []
        values = []
        for i, item in enumerate(data):
            # Verificar que todos los registros tengan las mismas columnas
            if set(item.keys()) != set(columns):
                raise ValidationError("Todos los registros deben tener las mismas columnas")
            
            # Crear los placeholders para este registro
            row_placeholders = [f"${len(values) + j + 1}" for j in range(len(columns))]
            placeholders.append(f"({', '.join(row_placeholders)})")
            
            # Agregar valores en el orden correcto
            values.extend(item[col] for col in columns)

        query = f"""
            INSERT INTO "{self._schema}"."{self._table}" 
            ({', '.join(f'"{col}"' for col in columns)})
            VALUES {', '.join(placeholders)}
        """

        if skipDuplicates:
            query += " ON CONFLICT DO NOTHING"
        
        try:
            await self._db.driver.execute(query, *values)
            return {"count": len(data)}
        except Exception as e:
            logger.error(f"Error en createMany: {e}")
            raise

class SchemaClient:
    """
    Proporciona acceso a las tablas de un schema específico.
    Las tablas se crean dinámicamente como atributos.
    """
    def __init__(self, db: 'GroovinDB', database: str, schema: str):
        self._db = db
        self._database = database
        self._schema = schema
        self._tables = {}

    def __getattr__(self, table: str) -> Table:
        if table not in self._tables:
            self._tables[table] = Table(self._db, self._database, self._schema, table)
        return self._tables[table]

    def __dir__(self) -> List[str]:
        """Lista los schemas disponibles"""
        default_attrs = super().__dir__()
        # Aquí deberíamos obtener los schemas de la base de datos
        # Por ahora retornamos solo los atributos por defecto
        return default_attrs

class DatabaseClient:
    """
    Proporciona acceso a los schemas de una base de datos específica.
    """
    def __init__(self, db: 'GroovinDB', database: str):
        self._db = db
        self._database = database
        self._schema_clients = {}

    def __getattr__(self, schema: str) -> SchemaClient:
        if schema not in self._schema_clients:
            self._schema_clients[schema] = SchemaClient(self._db, self._database, schema)
        return self._schema_clients[schema]

    async def get_schemas(self) -> List[str]:
        """Obtiene la lista de schemas disponibles"""
        await self._db._ensure_connected(self._database)
        driver = self._db._drivers[self._database]
        
        if hasattr(driver, '_introspect_postgresql'):
            query = """
            SELECT nspname as schema_name 
            FROM pg_namespace 
            WHERE nspname NOT IN ('information_schema', 'pg_catalog')
            """
        elif hasattr(driver, '_introspect_mysql'):
            query = "SHOW DATABASES"
        else:
            return []
            
        results = await driver.fetch(query)
        return [r['schema_name'] if 'schema_name' in r else r['Database'] for r in results]

    def __dir__(self) -> List[str]:
        """Lista los schemas disponibles"""
        default_attrs = super().__dir__()
        # Por ahora retornamos solo los atributos por defecto
        # La implementación completa requeriría una llamada asíncrona
        return default_attrs

    async def query(self, query: str, *args) -> List[Dict[str, Any]]:
        """Ejecuta una consulta SQL raw"""
        await self._db._ensure_connected(self._database)
        return await self._db._drivers[self._database].fetch(query, *args)

    async def execute(self, query: str, *args) -> None:
        """Ejecuta una query sin retornar resultados"""
        await self._db._ensure_connected(self._database)
        await self._db._drivers[self._database].execute(query, *args)

    async def query_one(self, query: str, *args) -> Optional[Dict[str, Any]]:
        """Ejecuta una query y retorna un único resultado"""
        await self._db._ensure_connected(self._database)
        return await self._db._drivers[self._database].fetch_one(query, *args)

class Client:
    """
    Proporciona acceso a las bases de datos configuradas en groovindb.json
    """
    def __init__(self, db: 'GroovinDB'):
        self._db = db
        self._database_clients = {}

    def __getattr__(self, database: str) -> 'DatabaseClient':
        if database not in self._db.config['connections']:
            available = list(self._db.config['connections'].keys())
            raise AttributeError(f"Conexión '{database}' no configurada. Conexiones disponibles: {', '.join(available)}")
        
        if database not in self._database_clients:
            self._database_clients[database] = DatabaseClient(self._db, database)
        return self._database_clients[database]

    def __dir__(self) -> List[str]:
        """Lista las conexiones disponibles"""
        default_attrs = super().__dir__()
        if hasattr(self, '_db') and hasattr(self._db, 'config'):
            connections = list(self._db.config['connections'].keys())
            return list(set(default_attrs + connections))
        return default_attrs
