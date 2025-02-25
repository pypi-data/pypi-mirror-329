from typing import Type
from .base import BaseDriver
from .postgresql import PostgreSQLDriver
from .mysql import MySQLDriver
from .sqlite import SQLiteDriver
def get_driver(driver_type: str) -> Type[BaseDriver]:
    """Retorna la clase del driver según el tipo"""
    drivers = {
        'postgresql': PostgreSQLDriver,
        'mysql': MySQLDriver,
        'sqlite': SQLiteDriver
    }
    
    if driver_type not in drivers:
        raise ValueError(f"Driver no soportado: {driver_type}. Drivers disponibles: {', '.join(drivers.keys())}")
    
    return drivers[driver_type] 