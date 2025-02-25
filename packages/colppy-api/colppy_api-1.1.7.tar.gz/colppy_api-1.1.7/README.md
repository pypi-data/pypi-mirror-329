# Colppy API Client

Cliente Python para la API de Colppy, sistema de gestión contable y financiera.

## Instalación

```bash
pip install colppy-api
```

## Configuración

El paquete incluye una CLI para facilitar la configuración inicial:

```bash
# Crear archivo de configuración interactivamente
colppy-api init
```

O puedes crear manualmente un archivo `config.json` en el directorio raíz de tu proyecto:

```json
{
  "ColppyAPI": {
    "COLPPY_API_URI": "https://login.colppy.com/lib/frontera2/service.php",
    "COLPPY_AUTH_USER": "tu_usuario",
    "COLPPY_AUTH_PASSWORD": "tu_password",
    "COLPPY_PARAMS_USER": "tu_usuario_params",
    "COLPPY_PARAMS_PASSWORD": "tu_password_params"
  },
  "LogLevel": {
    "LOG_LEVEL": "DEBUG"
  }
}
```

## Uso Básico

```python
from colppy import ColppyAPIClient

async def main():
    # Inicializar cliente
    client = ColppyAPIClient()
    await client.get_token()

    # Ejemplo: Obtener empresas
    empresas = await client.get_empresas()
    
    await client.logout()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
```

## Funcionalidades Principales

- Gestión de empresas
- Gestión de clientes
- Gestión de proveedores
- Comprobantes de compra y venta
- Movimientos contables
- Manejo de sesiones

## Tipos de Comprobantes

| ID | Código | Descripción               |
|----|--------|---------------------------|
| 1  | FAC    | Factura de Compra        |
| 2  | NCC    | Nota de Crédito Compra   |
| 3  | NDC    | Nota de Débito Compra    |
| 4  | FAV    | Factura de Venta         |
| 5  | NCV    | Nota de Crédito Venta    |
| 6  | NDV    | Nota de Débito Venta     |
| 7  | FCC    | Factura Compra Contado   |
| 8  | FVC    | Factura Venta Contado    |

## Desarrollo

Para contribuir al desarrollo:

```bash
# Clonar repositorio
git clone https://github.com/groovinads/colppy-api.git

# Crear entorno virtual
python -m venv .venv

# Activar entorno virtual
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows

# Instalar en modo desarrollo
pip install -e .
```

### Scripts de Desarrollo

```bash
# Publicar en PyPI
python scripts/run.py publish

# Limpiar caché
python scripts/run.py clean-cache

# Limpiar proyecto
python scripts/run.py clean

# Ejecutar todo
python scripts/run.py all
```

### Comandos CLI

```bash
# Inicializar configuración
colppy-api init

# Ver ayuda
colppy-api --help
```

## Licencia

MIT License

