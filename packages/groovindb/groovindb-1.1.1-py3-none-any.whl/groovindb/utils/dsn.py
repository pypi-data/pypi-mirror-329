from typing import Dict, Any
from urllib.parse import quote_plus

def build_dsn(config: Dict[str, Any]) -> str:
    """Construye el DSN según el driver"""
    driver = config.get('driver', 'postgresql')
    
    if driver == 'sqlite':
        return f"sqlite:///{config['database']}"
        
    password = quote_plus(str(config.get('password', '')))
    
    if driver == 'postgresql':
        return f"postgresql://{config['user']}:{password}@{config['host']}:{config['port']}/{config['database']}"
    elif driver == 'mysql':
        return f"mysql://{config['user']}:{password}@{config['host']}:{config['port']}/{config['database']}"
    
    raise ValueError(f"Driver no soportado: {driver}") 