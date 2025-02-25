# Colppy API Development Guide

## Estructura del Proyecto

```
colppy-api/
├── colppy/
│   ├── __init__.py
│   ├── cli/
│   │   ├── __init__.py
│   │   └── main.py
│   ├── operations/
│   │   ├── __init__.py
│   │   └── main.py
│   ├── helpers/
│   │   ├── __init__.py
│   │   ├── date.py
│   │   ├── errors.py
│   │   ├── logger.py
│   │   ├── formatters.py
│   │   └── data_frames.py
│   └── models/
│       ├── __init__.py
│       ├── auth.py
│       ├── clientes.py
│       ├── comprobantes_compra.py
│       ├── comprobantes_venta.py
│       ├── comprobante_compra_details.py
│       ├── comprobante_venta_details.py
│       ├── empresas.py
│       └── proveedores.py
├── scripts/
│   ├── clean.py
│   ├── clean_cache.py
│   ├── publish.py
│   └── run.py
├── pyproject.toml
├── setup.py
├── README.md
├── DEVELOPMENT.md
└── LICENSE
```

## Apéndice Técnico de Colppy

### Estados de Factura

| ID | Estado                |
|----|----------------------|
| 1  | Borrador            |
| 3  | Aprobada            |
| 4  | Anulada             |
| 5  | Pagada              |
| 6  | Parcialmente cobrada|
| 7  | Parcialmente pagada |

### Tipos de Factura

| Tipo | Código |
|------|--------|
| A    | 0      |
| B    | 1      |
| C    | 2      |
| E    | 3      |
| Z    | 4      |
| I    | 5      |
| M    | 6      |
| X    | 7      |
| T    | 8      |

### Lógica de Comprobantes

```
Clientes / Proveedores
├── Compras
│   ├── Proveedor
│   │   ├── FAC (Factura de Compra)
│   │   │   ├── ADG → Registro de Pago a Proveedor
│   │   │   └── OPAG → Registro de Otras Obligaciones
│   │   ├── NCC (Nota de Crédito de Compra)
│   │   ├── NDC (Nota de Débito de Compra)
│   │   └── FCC (Factura de Compra Contado)
└── Ventas
    ├── Cliente
    │   ├── FAV (Factura de Venta)
    │   │   ├── ACOB → Registro de Cobro a Cliente
    │   │   └── OCOB → Registro de Otras Obligaciones
    │   ├── NCV (Nota de Crédito de Venta)
    │   ├── NDV (Nota de Débito de Venta)
    │   └── FVC (Factura de Venta Contado)
```

### Movimientos

Los movimientos en Colppy se identifican por su `idTabla`. Los tipos principales son:

| idTabla | Descripción      | Códigos            |
|---------|------------------|-------------------|
| 8       | Factura Compra   | FCC, FAC, NDC, NCC|
| 14      | Orden de Pago    | OP                |
| 19      | Factura Venta    | FAV, FVC, NDV, NCV|
| 24      | Asiento Diario   | ADG               |
| 25      | Otros Pagos      | OPAG              |

Para más información sobre movimientos, consultar la [documentación oficial de Colppy](https://colppy.atlassian.net/wiki/spaces/CA/pages/141328409/Operaci+n+listar_movimientosdiario).

### Condiciones de Pago

Las condiciones de pago se expresan en días:
- Contado
- 15 días
- 30 días
- etc.

## Guías de Desarrollo

### Convenciones de Código

- Usar tipado estático con type hints
- Documentar clases y métodos con docstrings
- Seguir PEP 8 para estilo de código
- Usar async/await para operaciones de API

### Manejo de Errores

Los errores se manejan a través de la clase `ColppyError` en `helpers/errors.py`. Todos los errores de la API deben ser capturados y procesados apropiadamente.

### Logging

El sistema de logging está configurado en `helpers/logger.py` y soporta múltiples niveles:
- DEBUG
- INFO
- WARNING
- ERROR
- CRITICAL

### Testing

Por implementar:
- Tests unitarios
- Tests de integración
- Tests de la CLI 