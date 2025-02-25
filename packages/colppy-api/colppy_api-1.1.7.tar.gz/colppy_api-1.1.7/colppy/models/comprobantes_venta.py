from dataclasses import dataclass, field

from colppy.helpers.errors import ColppyError
from colppy.helpers.formatters import BaseModel


@dataclass(init=False)
class ComprobanteVenta(BaseModel):
    id_factura: str = field(metadata={"alias": "idFactura"}, default=None)
    id_tipo_factura: str = field(metadata={"alias": "idTipoFactura"}, default=None)
    fecha_pago: str = field(metadata={"alias": "fechaPago"}, default=None)
    id_tipo_comprobante: str = field(metadata={"alias": "idTipoComprobante"}, default=None)
    id_cliente: str = field(metadata={"alias": "idCliente"}, default=None)
    id_orden: str = field(metadata={"alias": "idOrden"}, default=None)
    nro_factura: str = field(metadata={"alias": "nroFactura"}, default=None)
    id_moneda: str = field(metadata={"alias": "idMoneda"}, default=None)
    fecha_factura: str = field(metadata={"alias": "fechaFactura"}, default=None)
    id_condicion_pago: str = field(metadata={"alias": "idCondicionPago"}, default=None)
    descripcion: str = field(metadata={"alias": "descripcion"}, default=None)
    id_estado_factura: int = field(metadata={"alias": "idEstadoFactura"}, default=None)
    total_factura: str = field(metadata={"alias": "totalFactura"}, default=None)
    id_ret_ganancias: str = field(metadata={"alias": "idRetGanancias"}, default=None)
    iibb_local: str = field(metadata={"alias": "IIBBLocal"}, default=None)
    iibb_otro: str = field(metadata={"alias": "IIBBOtro"}, default=None)
    iva_105: str = field(metadata={"alias": "IVA105"}, default=None)
    iva_21: str = field(metadata={"alias": "IVA21"}, default=None)
    iva_27: str = field(metadata={"alias": "IVA27"}, default=None)
    neto_gravado: str = field(metadata={"alias": "netoGravado"}, default=None)
    neto_no_gravado: str = field(metadata={"alias": "netoNoGravado"}, default=None)
    percepcion_iibb: str = field(metadata={"alias": "percepcionIIBB"}, default=None)
    percepcion_iibb1: str = field(metadata={"alias": "percepcionIIBB1"}, default=None)
    percepcion_iibb2: str = field(metadata={"alias": "percepcionIIBB2"}, default=None)
    percepcion_iva: str = field(metadata={"alias": "percepcionIVA"}, default=None)
    total_iva: str = field(metadata={"alias": "totalIVA"}, default=None)
    valor_cambio: str = field(metadata={"alias": "valorCambio"}, default=None)
    total_aplicado: str = field(metadata={"alias": "totalaplicado"}, default=None)
    cae: str = field(metadata={"alias": "cae"}, default=None)
    fecha_fe: str = field(metadata={"alias": "fechaFe"}, default=None)
    id_currency: str = field(metadata={"alias": "idCurrency"}, default=None)
    rate: str = field(metadata={"alias": "rate"}, default=None)
    record_insert_ts: str = field(metadata={"alias": "record_insert_ts"}, default=None)
    record_update_ts: str = field(metadata={"alias": "record_update_ts"}, default=None)
    is_mobile: str = field(metadata={"alias": "isMobile"}, default=None)
    razon_social: str = field(metadata={"alias": "RazonSocial"}, default=None)
    nombre_fantasia: str = field(metadata={"alias": "NombreFantasia"}, default=None)


class ComprobanteVentaRequest:
    def __init__(self, auth_user, auth_password, params_user, token, id_empresa, id_tipo_comprobante=None, filters=None,
                 order_fields=None,
                 order=None, start=0,
                 limit=100):
        self._auth_user = auth_user
        self._auth_password = auth_password
        self._params_user = params_user
        self._token = token
        self._id_empresa = id_empresa
        self._filters = [filters] if filters else []
        if id_tipo_comprobante:
            self._filters.append({
                "field": "idTipoComprobante",
                "op": "=",
                "value": id_tipo_comprobante
            })
        self._order_fields = order_fields if order_fields else ["idFactura"]
        self._order = order if order else "desc"
        self._start = start
        self._limit = limit

    def to_dict(self):
        return {
            "auth": {
                "usuario": self._auth_user,
                "password": self._auth_password
            },
            "service": {
                "provision": "FacturaVenta",
                "operacion": "listar_facturasventa"
            },
            "parameters": {
                "sesion": {
                    "usuario": self._params_user,
                    "claveSesion": self._token
                },
                "idEmpresa": self._id_empresa,
                "start": self._start,
                "limit": self._limit,
                "filter": self._filters,
                "order": {
                    "field": self._order_fields,
                    "order": self._order
                }
            }
        }


class ComprobanteVentaResponse:
    def __init__(self, response):
        self._response = response

    def get_comprobantes(self):
        if not ColppyError(self._response).is_error():
            if self._response['response']['data']:
                return [ComprobanteVenta(**comprobante) for comprobante in self._response['response']['data']]
        return []
