import os
import json
import click
from typing import Dict, Any

DEFAULT_CONFIG: Dict[str, Any] = {
    "ColppyAPI": {
        "COLPPY_API_URI": "https://login.colppy.com/lib/frontera2/service.php",
        "COLPPY_AUTH_USER": "",
        "COLPPY_AUTH_PASSWORD": "",
        "COLPPY_PARAMS_USER": "",
        "COLPPY_PARAMS_PASSWORD": ""
    },
    "LogLevel": {
        "LOG_LEVEL": "DEBUG"
    }
}

@click.group()
def cli():
    """CLI para la gestión de Colppy API"""
    pass

@cli.command()
def init():
    """Inicializa un nuevo archivo de configuración"""
    config_path = os.path.join(os.getcwd(), 'config.json')
    
    if os.path.exists(config_path):
        if not click.confirm('Ya existe un archivo config.json. ¿Deseas sobrescribirlo?'):
            click.echo('Operación cancelada')
            return

    click.echo('Configurando Colppy API...')
    
    config = DEFAULT_CONFIG.copy()
    config['ColppyAPI']['COLPPY_AUTH_USER'] = click.prompt('Usuario de autenticación', type=str)
    config['ColppyAPI']['COLPPY_AUTH_PASSWORD'] = click.prompt('Contraseña de autenticación', type=str, hide_input=True)
    config['ColppyAPI']['COLPPY_PARAMS_USER'] = click.prompt('Usuario de parámetros', type=str)
    config['ColppyAPI']['COLPPY_PARAMS_PASSWORD'] = click.prompt('Contraseña de parámetros', type=str, hide_input=True)
    
    log_level = click.prompt(
        'Nivel de log',
        type=click.Choice(['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'], case_sensitive=False),
        default='DEBUG'
    )
    config['LogLevel']['LOG_LEVEL'] = log_level

    with open(config_path, 'w') as f:
        json.dump(config, f, indent=2)
    
    click.echo('Archivo config.json creado exitosamente')

if __name__ == '__main__':
    cli() 