from typing import TypeVar, Dict, List, Union, Literal, Any, Optional
from datetime import datetime, date
from decimal import Decimal

# Tipos básicos
ID = Union[int, str]
JSON = Dict[str, Any]
Timestamp = Union[datetime, str]
DateType = Union[date, str]
Number = Union[int, float, Decimal]

# Operadores de comparación extendidos
ComparisonOperator = Literal[
    "equals", "not",
    "in", "notIn",
    "lt", "lte", "gt", "gte",
    "contains", "notContains",
    "startsWith", "endsWith",
    "between", "notBetween",
    "isNull", "isNotNull"
]

# Operadores de ordenamiento
SortOrder = Literal["asc", "desc"]

# Tipos de entrada mejorados
WhereInput = Dict[str, Union[Any, Dict[ComparisonOperator, Any]]]
OrderByInput = Dict[str, SortOrder]
SelectInput = Dict[str, bool]
CreateInput = Dict[str, Any]
UpdateInput = Dict[str, Any]
AggregateInput = Dict[str, List[str]]

# Tipos para transacciones
class Transaction:
    """Clase para manejar transacciones"""
    def __init__(self, driver: 'Driver'):
        self._driver = driver

    async def __aenter__(self):
        await self._driver.begin()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            await self._driver.rollback()
        else:
            await self._driver.commit() 