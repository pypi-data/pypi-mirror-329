from dataclasses import dataclass, field
from typing import List

from colppy.helpers.errors import ColppyError
from colppy.helpers.formatters import BaseModel


@dataclass(init=False)
class ComprobanteCompraDetailsItem(BaseModel):
    descripcion: str = field(metadata={"alias": "Descripcion"}, default=None)
    unidad_medida: str = field(metadata={"alias": "unidadMedida"}, default=None)
    cantidad: str = field(metadata={"alias": "Cantidad"}, default=None)
    inporte_unitario: str = field(metadata={"alias": "ImporteUnitario"}, default=None)
    iva: str = field(metadata={"alias": "IVA"}, default=None)
    id_plan_cuenta: str = field(metadata={"alias": "idPlanCuenta"}, default=None)
    desc_plan_cuenta: str = field(metadata={"alias": "descPlanCuenta"}, default=None)
    id_item: str = field(metadata={"alias": "idItem"}, default=None)
    id_almacen: str = field(metadata={"alias": "idAlmacen"}, default=None)
    ccosto1: str = field(metadata={"alias": "ccosto1"}, default=None)
    ccosto2: str = field(metadata={"alias": "ccosto2"}, default=None)
    porc_desc: str = field(metadata={"alias": "porcDesc"}, default=None)
    sub_total: str = field(metadata={"alias": "SubTotal"}, default=None)


@dataclass(init=False)
class ComprobanteCompraDetails(BaseModel):
    id_factura: str = field(metadata={"alias": "idFactura"}, default=None)
    id_proveedor: str = field(metadata={"alias": "idProveedor"}, default=None)
    id_empresa: str = field(metadata={"alias": "idEmpresa"}, default=None)
    id_estado_anterior: str = field(metadata={"alias": "idEstadoAnterior"}, default=None)
    fecha_factura: str = field(metadata={"alias": "fechaFactura"}, default=None)
    fecha_factura_doc: str = field(metadata={"alias": "fechaFacturaDoc"}, default=None)
    id_tipo_comprobante: str = field(metadata={"alias": "idTipoComprobante"}, default=None)
    id_tipo_factura: str = field(metadata={"alias": "idTipoFactura"}, default=None)
    nro_factura: str = field(metadata={"alias": "nroFactura"}, default=None)
    id_condicion_pago: str = field(metadata={"alias": "idCondicionPago"}, default=None)
    fecha_pago: str = field(metadata={"alias": "fechaPago"}, default=None)
    id_estado_factura: str = field(metadata={"alias": "idEstadoFactura"}, default=None)
    id_moneda: str = field(metadata={"alias": "idMoneda"}, default=None)
    valor_cambio: str = field(metadata={"alias": "valorCambio"}, default=None)
    id_currency: str = field(metadata={"alias": "idCurrency"}, default=None)
    rate: str = field(metadata={"alias": "rate"}, default=None)
    currency_iso: str = field(metadata={"alias": "currencyIso"}, default=None)
    currency_desc: str = field(metadata={"alias": "currencyDesc"}, default=None)
    id_ret_ganancias: str = field(metadata={"alias": "idRetGanancias"}, default=None)
    descripcion: str = field(metadata={"alias": "descripcion"}, default=None)
    neto_gravado: str = field(metadata={"alias": "netoGravado"}, default=None)
    neto_no_gravado: str = field(metadata={"alias": "netoNoGravado"}, default=None)
    total_iva: str = field(metadata={"alias": "totalIVA"}, default=None)
    iva_21: str = field(metadata={"alias": "IVA21"}, default=None)
    iva_105: str = field(metadata={"alias": "IVA105"}, default=None)
    iva_27: str = field(metadata={"alias": "IVA27"}, default=None)
    percepcion_iva: str = field(metadata={"alias": "percepcionIVA"}, default=None)
    percepcion_iibb: str = field(metadata={"alias": "percepcionIIBB"}, default=None)
    iibb_local: str = field(metadata={"alias": "IIBBLocal"}, default=None)
    percepcion_iibb1: str = field(metadata={"alias": "percepcionIIBB1"}, default=None)
    iibb_otro: str = field(metadata={"alias": "IIBBOtro"}, default=None)
    percepcion_iibb2: str = field(metadata={"alias": "percepcionIIBB2"}, default=None)
    total_factura: str = field(metadata={"alias": "totalFactura"}, default=None)
    total_aplicado: str = field(metadata={"alias": "totalaplicado"}, default=None)
    id_condicion_iva: str = field(metadata={"alias": "idCondicionIva"}, default=None)
    rete: str = field(metadata={"alias": "RETE"}, default=None)
    email: str = field(metadata={"alias": "Email"}, default=None)
    retencion_ica: str = field(metadata={"alias": "retencionIca"}, default=None)
    retefuente_id: str = field(metadata={"alias": "retefuenteId"}, default=None)
    cuenta_imp_gan: str = field(metadata={"alias": "cuentaImpGan"}, default=None)
    saldo_a_aplicar: str = field(metadata={"alias": "saldoaaplicar"}, default=None)
    nro_factura1: str = field(metadata={"alias": "nroFactura1"}, default=None)
    nro_factura2: str = field(metadata={"alias": "nroFactura2"}, default=None)
    has_nc: str = field(metadata={"alias": "has_NC"}, default=None)
    items: List[ComprobanteCompraDetailsItem] = field(default_factory=list)


class ComprobanteCompraDetailsRequest:
    def __init__(self, auth_user, auth_password, params_user, token, id_empresa, id_comprobante):
        self._auth_user = auth_user
        self._auth_password = auth_password
        self._params_user = params_user
        self._token = token
        self._id_empresa = id_empresa
        self._id_comprobante = id_comprobante

    def to_dict(self):
        return {
            'auth': {
                'usuario': self._auth_user,
                'password': self._auth_password
            },
            'service': {
                'provision': 'FacturaCompra',
                'operacion': 'leer_facturacompra'
            },
            'parameters': {
                'sesion': {
                    'usuario': self._params_user,
                    'claveSesion': self._token
                },
                'idEmpresa': self._id_empresa,
                'idFactura': self._id_comprobante
            }
        }


class ComprobanteCompraDetailsResponse:
    def __init__(self, response):
        self._response = response

    def get_comprobante(self):
        if not ColppyError(self._response).is_error():
            if self._response['response']['infofactura']:
                items = self._response['response']['itemsFactura'] or []
                items_objets = [ComprobanteCompraDetailsItem(**item) for item in items]
                details = ComprobanteCompraDetails(**self._response['response']['infofactura'])
                details.items = items_objets
                return details
            return None
