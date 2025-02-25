from dataclasses import dataclass
from typing import Optional, Dict, Any
from pathlib import Path
import json
from urllib.parse import quote_plus
from .constants import DRIVER_DEFAULT_PORTS

@dataclass
class DatabaseConfig:
    driver: str
    host: str
    port: int
    database: str
    user: str
    password: str
    schema: str = 'public'
    ssl: bool = False
    ssl_ca: Optional[str] = None
    ssl_cert: Optional[str] = None
    ssl_key: Optional[str] = None
    connect_timeout: int = 10
    command_timeout: int = 30
    pool_min_size: int = 1
    pool_max_size: int = 10

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'DatabaseConfig':
        return cls(**data)

    @classmethod
    def from_file(cls, path: str = "groovindb.json") -> 'DatabaseConfig':
        try:
            with open(path) as f:
                data = json.load(f)
            return cls.from_dict(data)
        except FileNotFoundError:
            raise ValueError(f"Archivo de configuración no encontrado: {path}")
        except json.JSONDecodeError:
            raise ValueError(f"Archivo de configuración inválido: {path}")

    def __post_init__(self):
        """Validar configuración"""
        if self.driver not in ['postgresql', 'mysql']:
            raise ValueError(f"Driver no soportado: {self.driver}")
        
        if not self.host:
            raise ValueError("Host no puede estar vacío")
            
        if not isinstance(self.port, int):
            try:
                self.port = int(self.port)
            except (TypeError, ValueError):
                raise ValueError(f"Puerto inválido: {self.port}")
        
        # Usar puerto por defecto si no se especifica
        if not self.port:
            self.port = DRIVER_DEFAULT_PORTS[self.driver]

    def get_dsn(self) -> str:
        """Retorna el DSN escapando caracteres especiales"""
        password = quote_plus(self.password) if self.password else ''
        user = quote_plus(self.user) if self.user else ''
        
        if self.driver == 'postgresql':
            return f"postgresql://{user}:{password}@{self.host}:{self.port}/{self.database}"
        else:
            return f"mysql://{user}:{password}@{self.host}:{self.port}/{self.database}" 