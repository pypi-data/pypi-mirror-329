# GroovinDB

GroovinDB es un ORM (Object-Relational Mapping) minimalista y eficiente para Python que soporta múltiples bases de datos (PostgreSQL, MySQL y SQLite). Proporciona una interfaz limpia y tipada para interactuar con bases de datos relacionales.

## Características

- Soporte para múltiples bases de datos simultáneas
- Manejo automático de múltiples schemas
- Soporte para PostgreSQL, MySQL y SQLite
- Queries raw específicas por tipo de base de datos
- Tipado estático con generación automática de tipos
- API intuitiva y fácil de usar
- CLI integrado para inicialización y generación de tipos
- Operaciones CRUD completas
- Validación de inputs
- Logging integrado con rotación de archivos
- Soporte para operaciones de agregación
- Manejo de transacciones
- Pool de conexiones configurable

## Instalación

```bash
pip install groovindb
```

## Configuración Rápida

1. Inicializa un nuevo proyecto:

```bash
groovindb init
```

Este comando creará un archivo `groovindb.json` donde puedes configurar múltiples conexiones:

```json
{
  "default": "postgresql",
  "connections": {
    "postgresql": {
      "driver": "postgresql",
      "host": "localhost",
      "port": 5432,
      "database": "warehouse",
      "user": "usuario",
      "password": "contraseña"
    },
    "mysql": {
      "driver": "mysql",
      "host": "localhost",
      "port": 3306,
      "database": "app_db",
      "user": "usuario",
      "password": "contraseña"
    }
  }
}
```

2. Genera los tipos de tus bases de datos:

```bash
groovindb introspect
```

## Uso Básico

```python
from groovindb import GroovinDB

async def main():
    # Inicializar la conexión
    db = GroovinDB()
    
    # Consultas raw en PostgreSQL
    pg_results = await db.client.postgresql.query(
        "SELECT * FROM schema.table WHERE id = $1",
        123
    )
    
    # Consultas raw en MySQL
    mysql_results = await db.client.mysql.query(
        "SELECT * FROM table WHERE active = %s",
        True
    )
    
    # Consulta que retorna una sola fila
    single_result = await db.client.postgresql.query_one(
        "SELECT * FROM users WHERE id = $1",
        123
    )
    
    # Ejecutar una query sin retorno
    await db.client.mysql.execute(
        "UPDATE users SET active = %s WHERE id = %s",
        True, 123
    )
    
    await db.disconnect()
```

## Manejo de Schemas

GroovinDB detecta y maneja automáticamente todos los schemas disponibles en tus bases de datos:

```python
# Acceso a tablas en diferentes schemas
pg_result = await db.client.postgresql.query(
    "SELECT * FROM public.users WHERE id = $1",
    123
)

mysql_result = await db.client.mysql.query(
    "SELECT * FROM app.products WHERE active = %s",
    True
)
```

## Tipos de Queries Raw

Cada driver de base de datos proporciona tres métodos principales:

```python
# Consulta que retorna múltiples filas
results = await db.client.postgresql.query(
    "SELECT * FROM users WHERE active = $1",
    True
)

# Consulta que retorna una sola fila
user = await db.client.postgresql.query_one(
    "SELECT * FROM users WHERE id = $1",
    123
)

# Ejecutar una query sin retorno
await db.client.postgresql.execute(
    "UPDATE users SET active = $1 WHERE id = $2",
    True, 123
)
```

## Placeholders por Driver

Cada driver utiliza su propio estilo de placeholders:

- PostgreSQL: `$1`, `$2`, etc.
- MySQL: `%s`
- SQLite: `?`

## Logging Mejorado

```python
from groovindb.utils.logger import logger

# Configuración básica
logger.setLevel("DEBUG")

# Configuración avanzada con rotación de archivos
from groovindb.utils.logger import GroovinLogger

logger = GroovinLogger(
    name="mi_app",
    level="DEBUG",
    log_file="app.log",
    rotate=True,
    max_bytes=10_000_000,  # 10MB
    backup_count=5
).logger
```

## Configuración SSL

```json
{
  "connections": {
    "postgresql": {
      "ssl": true,
      "ssl_ca": "/path/to/ca.crt",
      "ssl_cert": "/path/to/client-cert.pem",
      "ssl_key": "/path/to/client-key.pem"
    }
  }
}
```

## Pool de Conexiones

```json
{
  "connections": {
    "postgresql": {
      "pool_min_size": 1,
      "pool_max_size": 10,
      "connect_timeout": 10,
      "command_timeout": 30
    }
  }
}
```

## Soporte de Drivers

- PostgreSQL (usando `asyncpg`)
- MySQL (usando `aiomysql`)
- SQLite (usando `aiosqlite`)

## Consideraciones de Rendimiento

- Pool de conexiones configurable por base de datos
- Conexiones manejadas automáticamente
- Queries validadas antes de ser ejecutadas
- Soporte para transacciones
- Timeouts configurables
- Rotación de logs para mejor rendimiento

## Licencia

MIT License - ver archivo [LICENSE](LICENSE) para más detalles.