from typing import Dict, Any, Optional, List
from groovindb.core.client import Table

class Client:
    clientes: Table
    cobranzas: Table
    empresas: Table
    facturas_a_cobrar: Table
    facturas_a_pagar: Table
    movimientos: Table
    pagos: Table
    proveedores: Table
    tesoreria: Table

    def __init__(self, db):
        self._db = db
        self.clientes = Table(db, 'clientes')
        self.cobranzas = Table(db, 'cobranzas')
        self.empresas = Table(db, 'empresas')
        self.facturas_a_cobrar = Table(db, 'facturas_a_cobrar')
        self.facturas_a_pagar = Table(db, 'facturas_a_pagar')
        self.movimientos = Table(db, 'movimientos')
        self.pagos = Table(db, 'pagos')
        self.proveedores = Table(db, 'proveedores')
        self.tesoreria = Table(db, 'tesoreria')
