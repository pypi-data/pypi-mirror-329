import click
import json
import asyncio
from .core.db import GroovinDB
from .core.constants import DRIVER_DEFAULT_PORTS
import os
import sys

@click.group()
def cli():
    """GroovinDB CLI"""
    pass

@cli.command()
@click.option('--database', help='Nombre de la conexión a usar')
@click.option('--driver', type=click.Choice(['postgresql', 'mysql', 'sqlite']), help='Driver de base de datos')
@click.option('--host', help='Host de la base de datos')
@click.option('--port', type=int, help='Puerto de la base de datos')
@click.option('--dbname', help='Nombre de la base de datos')
@click.option('--user', help='Usuario de la base de datos')
@click.option('--password', help='Contraseña de la base de datos')
def init(database, driver, host, port, dbname, user, password):
    """Inicializa un nuevo proyecto GroovinDB"""
    try:
        # Cargar configuración existente o crear nueva
        if os.path.exists("groovindb.json"):
            with open("groovindb.json", "r") as f:
                config = json.load(f)
        else:
            config = {
                "default": None,
                "connections": {}
            }

        while True:
            # Si no se proporcionan argumentos, usar modo interactivo
            if not all([database, driver]):
                database = click.prompt('Nombre de la conexión', default='default')
                driver = click.prompt(
                    'Driver',
                    type=click.Choice(['postgresql', 'mysql', 'sqlite']),
                    default='postgresql'
                )

            # Configuración según el driver
            conn_config = {'driver': driver}
            
            if driver == 'sqlite':
                conn_config['database'] = click.prompt(
                    'Database path',
                    default='./database.sqlite'
                ) if not dbname else dbname
            else:
                conn_config.update({
                    'host': host or click.prompt('Host', default='localhost'),
                    'port': port or click.prompt('Port', type=int, 
                        default=3306 if driver == 'mysql' else 5432),
                    'database': dbname or click.prompt('Database'),
                    'user': user or click.prompt('User'),
                    'password': password or click.prompt('Password', hide_input=True)
                })

            # Actualizar configuración
            config['connections'][database] = conn_config
            if not config['default']:
                config['default'] = database

            click.echo(f"✅ Configuración creada para {database}")

            # Preguntar si quiere agregar otra base de datos
            if not click.confirm('¿Deseas agregar otra base de datos?', default=False):
                break
                
            # Reset de variables para la siguiente iteración
            database = driver = host = port = dbname = user = password = None

        # Guardar configuración final
        with open("groovindb.json", "w") as f:
            json.dump(config, f, indent=2)

        if click.confirm('¿Deseas generar los tipos automáticamente?', default=True):
            ctx = click.get_current_context()
            # Hacer introspección para cada conexión configurada
            for conn_name in config['connections'].keys():
                click.echo(f"\nGenerando tipos para {conn_name}...")
                ctx.invoke(introspect, database=conn_name)

    except Exception as e:
        click.echo(f"❌ Error: {str(e)}", err=True)
        sys.exit(1)

@cli.command()
@click.option('--database', help='Nombre de la conexión a usar')
def introspect(database: str = None):
    """Genera tipos basados en la estructura de la base de datos"""
    try:
        # Cargar configuración
        with open("groovindb.json", "r") as f:
            config = json.load(f)
        
        # Si no se especifica database, usar todas las conexiones
        databases = [database] if database else config['connections'].keys()
        
        async def run():
            db = GroovinDB()  # Crear una sola instancia de GroovinDB
            try:
                for db_name in databases:
                    click.echo(f"\nGenerando tipos para {db_name}...")
                    await db._ensure_connected(db_name)
                await db.introspect()
                click.echo("✅ Tipos generados exitosamente")
            except Exception as e:
                click.echo(f"❌ Error: {str(e)}", err=True)
            finally:
                await db.disconnect()

        asyncio.run(run())
        
    except Exception as e:
        click.echo(f"❌ Error: {str(e)}", err=True)
        sys.exit(1)

if __name__ == "__main__":
    cli() 