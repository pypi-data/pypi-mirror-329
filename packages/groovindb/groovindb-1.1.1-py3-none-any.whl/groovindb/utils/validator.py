from typing import Any, Dict, List, Optional
from ..types import (
    WhereInput, OrderByInput, SelectInput, CreateInput, UpdateInput,
    AggregateInput
)
from enum import Enum

class ValidationError(Exception):
    """Error de validación personalizado"""
    pass

class SortOrder(str, Enum):
    ASC = "asc"
    DESC = "desc"

# Definición unificada de operadores y sus mapeos SQL
OPERATORS = {
    "equals": "=",
    "not": "!=",
    "gt": ">",
    "gte": ">=",
    "lt": "<",
    "lte": "<=",
    "in": "IN",
    "notIn": "NOT IN",
    "contains": "LIKE",
    "notContains": "NOT LIKE",
    "startsWith": "LIKE",
    "endsWith": "LIKE",
    "between": "BETWEEN",
    "notBetween": "NOT BETWEEN"
}

# Operadores de agregación válidos
AGGREGATE_OPERATORS = ["_sum", "_avg", "_min", "_max", "_count"]

def validate_where(where: Optional[WhereInput]) -> None:
    """Valida condiciones WHERE"""
    if not where:
        return
    
    for field, condition in where.items():
        if isinstance(condition, dict):
            for op, value in condition.items():
                if op not in OPERATORS:
                    raise ValidationError(f"Operador inválido: {op}")
                
                # Validaciones específicas por operador
                if op in ["in", "notIn"] and not isinstance(value, (list, tuple)):
                    raise ValidationError(f"El operador {op} requiere una lista de valores")
                if op in ["between", "notBetween"] and not (
                    isinstance(value, (list, tuple)) and len(value) == 2
                ):
                    raise ValidationError(f"El operador {op} requiere exactamente 2 valores")

def validate_order_by(order_by: Optional[Dict[str, str]]) -> None:
    """Valida el parámetro order_by"""
    if order_by is None:
        return
        
    if not isinstance(order_by, dict):
        raise ValidationError("order_by debe ser un diccionario")
        
    for field, direction in order_by.items():
        if not isinstance(field, str):
            raise ValidationError("Las claves de order_by deben ser strings")
            
        if not isinstance(direction, str) or direction.lower() not in [SortOrder.ASC, SortOrder.DESC]:
            raise ValidationError("Los valores de order_by deben ser 'asc' o 'desc'")

def validate_select(select: Optional[SelectInput]) -> None:
    """Valida campos seleccionados"""
    if not select:
        return
    
    if not isinstance(select, dict):
        raise ValidationError("Select debe ser un diccionario")
    
    for field, include in select.items():
        if not isinstance(include, bool):
            raise ValidationError(f"Valor inválido en select para {field}")

def validate_aggregate(aggregate: Optional[AggregateInput]) -> None:
    """Valida operaciones de agregación"""
    if not aggregate:
        return
    
    for op, fields in aggregate.items():
        if op not in AGGREGATE_OPERATORS:
            raise ValidationError(f"Operador de agregación inválido: {op}")
        if not isinstance(fields, list):
            raise ValidationError(f"Los campos para {op} deben ser una lista")

def validate_input(
    where: Optional[Dict[str, Any]] = None,
    data: Optional[Dict[str, Any]] = None,
    order_by: Optional[Dict[str, str]] = None,
    select: Optional[Dict[str, bool]] = None,
    take: Optional[int] = None,
    skip: Optional[int] = None
) -> None:
    """Valida los parámetros de entrada"""
    if where is not None:
        validate_where(where)
    if data is not None:
        validate_data(data)
    if order_by is not None:
        validate_order_by(order_by)
    if select is not None:
        validate_select(select)
    if take is not None:
        validate_take(take)
    if skip is not None:
        validate_skip(skip) 

def validate_take(take: Optional[int]) -> None:
    """Valida el parámetro take (limit)"""
    if take is not None:
        if not isinstance(take, int):
            raise ValidationError("take debe ser un número entero")
        if take < 0:
            raise ValidationError("take no puede ser negativo")

def validate_skip(skip: Optional[int]) -> None:
    """Valida el parámetro skip (offset)"""
    if skip is not None:
        if not isinstance(skip, int):
            raise ValidationError("skip debe ser un número entero")
        if skip < 0:
            raise ValidationError("skip no puede ser negativo")

def validate_data(data: Dict[str, Any]) -> None:
    """Valida los datos para create/update"""
    if not isinstance(data, dict):
        raise ValidationError("data debe ser un diccionario")
    if not data:
        raise ValidationError("data no puede estar vacío") 

def validate_transaction(func):
    """Decorador para validar el contexto de transacción"""
    async def wrapper(self, *args, **kwargs):
        if not hasattr(self, '_in_transaction') or not self._in_transaction:
            raise ValidationError("Esta operación debe ejecutarse dentro de una transacción")
        return await func(self, *args, **kwargs)
    return wrapper

def validate_connection(func):
    """Decorador para validar la conexión"""
    async def wrapper(self, *args, **kwargs):
        if not hasattr(self, '_connected') or not self._connected:
            raise ValidationError("No hay conexión a la base de datos")
        return await func(self, *args, **kwargs)
    return wrapper 