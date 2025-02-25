from typing import Dict, Any

DEFAULT_CONFIG: Dict[str, Any] = {
    "driver": "postgresql",
    "host": "localhost",
    "port": 5432,
    "schema": "public",
}

DRIVER_DEFAULT_PORTS = {
    "postgresql": 5432,
    "mysql": 3306,
    "sqlite": None
} 
