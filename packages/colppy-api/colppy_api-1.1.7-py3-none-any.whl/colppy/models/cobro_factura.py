from dataclasses import dataclass, field

from colppy.helpers.errors import ColppyError
from colppy.helpers.formatters import BaseModel


@dataclass(init=False)
class CobroFactura(BaseModel):
    id_empresa: str = field(metadata={"alias": "idEmpresa"}, default=None)
    id_tabla: str = field(metadata={"alias": "idTabla"}, default=None)
    id_elemento: str = field(metadata={"alias": "idElemento"}, default=None)
    id_diario: str = field(metadata={"alias": "idDiario"}, default=None)
    id_elemento_contacto: str = field(metadata={"alias": "idElementoContacto"}, default=None)
    id_objeto_contacto: str = field(metadata={"alias": "idObjetoContacto"}, default=None)
    fecha_contabilizado: str = field(metadata={"alias": "FechaContabilizado"}, default=None)
    fecha_contable: str = field(metadata={"alias": "fechaContable"}, default=None)
    id_plan_cuenta: str = field(metadata={"alias": "idPlanCuenta"}, default=None)
    id_subdiario: str = field(metadata={"alias": "idSubdiario"}, default=None)
    debito_credito: str = field(metadata={"alias": "DebitoCredito"}, default=None)
    importe: str = field(metadata={"alias": "Importe"}, default=None)
    id_tabla_aplicado: str = field(metadata={"alias": "idTablaAplicado"}, default=None)
    id_elemento_aplicado: str = field(metadata={"alias": "idElementoAplicado"}, default=None)
    id_item: str = field(metadata={"alias": "idItem"}, default=None)
    id_item_aplicado: str = field(metadata={"alias": "idItemAplicado"}, default=None)
    ccosto1: str = field(metadata={"alias": "ccosto1"}, default=None)
    ccosto2: str = field(metadata={"alias": "ccosto2"}, default=None)
    conciliado: str = field(metadata={"alias": "Conciliado"}, default=None)
    batch: str = field(metadata={"alias": "batch"}, default=None)
    id_tercero: str = field(metadata={"alias": "idTercero"}, default=None)
    is_niif: str = field(metadata={"alias": "isNIIF"}, default=None)
    item_id: str = field(metadata={"alias": "itemId"}, default=None)
    id_cobro: str = field(metadata={"alias": "idCobro"}, default=None)
    nro_recibo: str = field(metadata={"alias": "nroRecibo"}, default=None)
    id_cliente: str = field(metadata={"alias": "idCliente"}, default=None)
    fecha_cobro: str = field(metadata={"alias": "fechaCobro"}, default=None)
    valor_cambio: str = field(metadata={"alias": "valorCambio"}, default=None)
    total_cobro: str = field(metadata={"alias": "totalCobro"}, default=None)
    id_estado_cobro: str = field(metadata={"alias": "idEstadoCobro"}, default=None)
    anticipo: str = field(metadata={"alias": "anticipo"}, default=None)
    descuentos: str = field(metadata={"alias": "descuentos"}, default=None)
    intereses: str = field(metadata={"alias": "intereses"}, default=None)
    ret_ganancias: str = field(metadata={"alias": "retGanancias"}, default=None)
    ret_iva: str = field(metadata={"alias": "retIVA"}, default=None)
    ret_suss: str = field(metadata={"alias": "retSUSS"}, default=None)
    retencion_iibb: str = field(metadata={"alias": "retencionIIBB"}, default=None)
    retencion_iibb1: str = field(metadata={"alias": "retencionIIBB1"}, default=None)
    retencion_iibb2: str = field(metadata={"alias": "retencionIIBB2"}, default=None)
    iibb_local: str = field(metadata={"alias": "IIBBLocal"}, default=None)
    iibb_otro: str = field(metadata={"alias": "IIBBOtro"}, default=None)
    total_cobrado: str = field(metadata={"alias": "totalCobrado"}, default=None)
    retencion_otras: str = field(metadata={"alias": "retencionOtras"}, default=None)
    descripcion: str = field(metadata={"alias": "descripcion"}, default=None)
    este_cobro: str = field(metadata={"alias": "esteCobro"}, default=None)
    diferencia_tipo_cambio: str = field(metadata={"alias": "diferenciaTipoCambio"}, default=None)


class CobroFacturaRequest:
    def __init__(self, auth_user, auth_password, params_user, token, id_empresa, id_factura):
        self._auth_user = auth_user
        self._auth_password = auth_password
        self._params_user = params_user
        self._token = token
        self._id_empresa = id_empresa
        self._id_factura = id_factura

    def to_dict(self):
        return {
            "auth": {
                "usuario": self._auth_user,
                "password": self._auth_password
            },
            "service": {
                "provision": "FacturaVenta",
                "operacion": "leer_cobros_factura"
            },
            "parameters": {
                "sesion": {
                    "usuario": self._params_user,
                    "claveSesion": self._token
                },
                "idEmpresa": self._id_empresa,
                "idFactura": self._id_factura
            }
        }


class CobroFacturaResponse:
    def __init__(self, response):
        self._response = response

    def get_cobro(self):
        if not ColppyError(self._response).is_error():
            if self._response['response']['data']:
                return [CobroFactura(**item) for item in self._response['response']['data']]
            return None
