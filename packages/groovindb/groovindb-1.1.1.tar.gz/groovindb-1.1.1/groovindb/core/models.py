from typing import Dict, Any, TypeVar, Type

T = TypeVar('T')


class Model:
    def __init__(self, data: Dict[str, Any]):
        for key, value in data.items():
            setattr(self, key, value)

    def __repr__(self):
        attrs = [f"{k}={repr(v)}" for k, v in self.__dict__.items()]
        return f"{self.__class__.__name__}({', '.join(attrs)})"


def create_model_class(name: str, fields: Dict[str, Type]) -> type:
    """Crea dinámicamente una clase de modelo con los campos especificados"""
    return type(name, (Model,), {
        '__annotations__': fields,
        '__slots__': list(fields.keys())
    })
