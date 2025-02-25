from pathlib import Path
from typing import Dict, Any, TYPE_CHECKING, List
import json
from .client import Client
from ..utils.dsn import build_dsn
from ..drivers import get_driver
from ..utils.introspector import DatabaseIntrospector
from ..utils.logger import logger

if TYPE_CHECKING:
    from db_types import GeneratedClient

class GroovinDB:
    def __init__(self):
        """Inicializa GroovinDB con todas las conexiones configuradas"""
        self._load_config()
        self._drivers = {}
        self._connected = set()
        self.schema_info = {}
        
        # Crear el cliente dinámico
        if TYPE_CHECKING:
            self.client: GeneratedClient
        else:
            self.client = Client(self)

    def _load_config(self) -> None:
        """Carga la configuración desde groovindb.json"""
        try:
            with open("groovindb.json", "r") as f:
                self.config = json.load(f)
                if 'connections' not in self.config:
                    raise ValueError("Formato de configuración inválido")
        except FileNotFoundError:
            raise FileNotFoundError("Archivo groovindb.json no encontrado")

    async def _ensure_connected(self, database: str) -> None:
        """Asegura que la conexión está establecida"""
        if database not in self._connected:
            config = self.config['connections'][database]
            dsn = build_dsn(config)
            driver = self.get_driver(database)
            await driver.connect(dsn)
            self._connected.add(database)
            logger.info(f"Conectado a {database}")

    async def disconnect(self):
        """Cierra todas las conexiones activas"""
        for driver in self._drivers.values():
            if driver:
                await driver.close()
        self._drivers = {}
        self._connected = set()  # Limpiamos también el set de conexiones
        logger.info("Desconectado de todas las bases de datos")

    def get_driver(self, database: str):
        """Obtiene el driver para una base de datos específica"""
        if database not in self._drivers:
            config = self.config['connections'][database]
            self._drivers[database] = get_driver(config.get('driver', 'postgresql'))()
        return self._drivers[database]

    async def connect(self):
        if self._connected:
            return

        try:
            # Construir DSN según el driver
            if self.config['driver'] == 'sqlite':
                dsn = f"sqlite:///{(self.config['database'])}"
            else:
                # DSN para PostgreSQL y MySQL
                dsn = f"{self.config['driver']}://{self.config['user']}:{self.config['password']}@{self.config['host']}:{self.config['port']}/{self.config['database']}"
            
            await self.driver.connect(dsn)
            self._connected = True
            
            # Obtener información de todos los schemas
            introspector = DatabaseIntrospector(self.driver)
            self.schema_info = await introspector.get_all_schemas_info()
            self.tables = set().union(*[set(tables.keys()) for tables in self.schema_info.values()])
            
            # Inicializar cliente después de tener las tablas
            self.client = Client(self)
            
            db_name = self.config['database']
            if self.config['driver'] != 'sqlite':
                db_name = f"{self.config['host']}:{self.config['port']}/{db_name}"
            
            logger.info(f"Conectado a {db_name} - Schemas encontrados: {list(self.schema_info.keys())}")
        
        except Exception as e:
            logger.error(f"Error al conectar: {e}")
            raise

    def sanitize_class_name(self, name: str) -> str:
        """Sanitiza nombres para clases de Python"""
        # Primero reemplazar caracteres especiales con guión bajo
        name = ''.join(c if c.isalnum() else '_' for c in name)
        # Eliminar guiones bajos múltiples
        while '__' in name:
            name = name.replace('__', '_')
        # Eliminar guiones al inicio/final
        name = name.strip('_')
        # Asegurar que empiece con mayúscula
        return name[0].upper() + name[1:] if name else name

    def _generate_table_type(self, type_name: str, info: Dict[str, Any]) -> List[str]:
        """Genera el código para un tipo de tabla"""
        code = []
        fields = info.get('fields', {})
        
        # Generar la clase del tipo
        code.append(f"class {type_name}:")
        if not fields:
            code.append("    pass")
        else:
            for field_name, field_info in fields.items():
                python_type = self._map_db_type(field_info['type'])
                nullable = field_info.get('nullable', True)
                type_annotation = f"Optional[{python_type}]" if nullable else python_type
                name = field_name.replace(' ', '_')
                code.append(f"    {name}: {type_annotation}")
        
        code.append("")  # Línea en blanco para separar clases
        return code

    def _generate_schema_client(self, database: str, schemas_info: Dict[str, Dict[str, Any]]) -> List[str]:
        """Genera el código para el cliente del schema"""
        code = []
        
        # Generar clases para cada schema
        for schema_name, schema_info in schemas_info.items():
            class_name = self.sanitize_class_name(f"{database}_{schema_name}_SchemaClient")
            code.append(f"class {class_name}(SchemaClient):")
            
            if not schema_info:
                code.append("    pass")
            else:
                for table_name in schema_info.keys():
                    type_name = self.sanitize_class_name(f"{database}_{schema_name}_{table_name}Type")
                    code.append(f"    {table_name}: Table[{type_name}]")
            
            code.append("")  # Línea en blanco para separar clases
        
        return code

    async def introspect(self):
        """Genera tipos basados en la estructura de todas las bases de datos"""
        code = [
            "from typing import Dict, Any, Optional, List, TypeVar",
            "from datetime import datetime, date",
            "from decimal import Decimal",
            "from groovindb.core.client import Table, Client, SchemaClient, DatabaseClient",
            "from groovindb.types import *\n",
            "T = TypeVar('T')\n"
        ]

        # Diccionario para almacenar las clases de schema por base de datos
        database_schemas = {}

        for database, config in self.config['connections'].items():
            try:
                await self._ensure_connected(database)
                driver = self._drivers[database]
                introspector = DatabaseIntrospector(driver)
                
                schemas_info = await introspector.get_all_schemas_info()
                logger.info(f"Schemas encontrados en {database}: {list(schemas_info.keys())}")
                
                database_schemas[database] = []
                
                # Generar tipos para cada tabla
                for schema_name, schema_info in schemas_info.items():
                    schema_tables = []
                    
                    for table_name, info in schema_info.items():
                        # Generar clase de tipo para la tabla
                        type_name = self.sanitize_class_name(f"{database}_{schema_name}_{table_name}Type")
                        code.extend(self._generate_table_type(type_name, info))
                        schema_tables.append((table_name, type_name))
                    
                    # Generar clase del schema
                    schema_class_name = self.sanitize_class_name(f"{database}_{schema_name}_SchemaClient")
                    code.extend([
                        f"class {schema_class_name}(SchemaClient):",
                        *[f"    {table}: 'Table[{type_name}]'" for table, type_name in schema_tables],
                        ""
                    ])
                    database_schemas[database].append((schema_name, schema_class_name))

            except Exception as e:
                logger.error(f"Error introspecting {database}: {str(e)}")
                continue

        # Generar clases de base de datos
        for database, schemas in database_schemas.items():
            db_class_name = self.sanitize_class_name(f"{database}_DatabaseClient")
            code.extend([
                f"class {db_class_name}(DatabaseClient):",
                *[f"    {schema}: {schema_class}" for schema, schema_class in schemas],
                ""
            ])

        # Generar la clase GeneratedClient
        # code.extend([
        #     "class GeneratedClient(Client):",
        #     *[f"    {db}: '{self.sanitize_class_name(f"{db}_DatabaseClient")}'"
        #       for db in database_schemas.keys()],
        #     ""
        # ])

        code.extend([
            "class GeneratedClient(Client):",
            *[f"    {db}: '{self.sanitize_class_name(db + '_DatabaseClient')}'"
              for db in database_schemas.keys()],
            ""
        ])

        # Escribir el archivo de tipos
        Path("db_types.py").write_text("\n".join(code))

    def _map_db_type(self, db_type: str) -> str:
        """Mapea tipos de base de datos a tipos de Python"""
        type_map = {
            'integer': 'int',
            'bigint': 'int',
            'smallint': 'int',
            'character varying': 'str',
            'varchar': 'str',
            'text': 'str',
            'boolean': 'bool',
            'timestamp': 'datetime',
            'timestamptz': 'datetime',
            'date': 'date',
            'numeric': 'Decimal',
            'decimal': 'Decimal',
            'real': 'float',
            'double precision': 'float',
            'json': 'Dict[str, Any]',
            'jsonb': 'Dict[str, Any]',
            'array': 'List[Any]',
        }
        return type_map.get(db_type.lower(), 'Any')