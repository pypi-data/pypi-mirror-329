from dataclasses import dataclass, field

from colppy.helpers.errors import ColppyError
from colppy.helpers.formatters import BaseModel


@dataclass(init=False)
class CompraPagoDetail(BaseModel):
    id_empresa: int = field(metadata={"alias": "idEmpresa"}, default=None)
    id_pago: int = field(metadata={"alias": "idPago"}, default=None)
    id_proveedor: int = field(metadata={"alias": "idProveedor"}, default=None)
    fecha_pago: str = field(metadata={"alias": "fechaPago"}, default=None)
    valor_cambio: float = field(metadata={"alias": "valorCambio"}, default=None)
    total_pagado: float = field(metadata={"alias": "totalpagado"}, default=None)
    retencion_iibb: float = field(metadata={"alias": "retencionIIBB"}, default=None)
    id_estado_pago: str = field(metadata={"alias": "idEstadoPago"}, default=None)
    anticipo: float = field(metadata={"alias": "anticipo"}, default=None)
    total_facturas: float = field(metadata={"alias": "totalFacturas"}, default=None)
    descuentos: float = field(metadata={"alias": "descuentos"}, default=None)
    intereses: float = field(metadata={"alias": "intereses"}, default=None)
    ret_ganancias1: float = field(metadata={"alias": "retGanancias1"}, default=None)
    ret_ganancias2: float = field(metadata={"alias": "retGanancias2"}, default=None)
    id_ret_ganancias1: int = field(metadata={"alias": "idRetGanancias1"}, default=None)
    id_ret_ganancias2: int = field(metadata={"alias": "idRetGanancias2"}, default=None)
    nro_pago: str = field(metadata={"alias": "nroPago"}, default=None)
    base_calculo1: float = field(metadata={"alias": "baseCalculo1"}, default=None)
    base_calculo2: float = field(metadata={"alias": "baseCalculo2"}, default=None)
    descripcion: str = field(metadata={"alias": "descripcion"}, default=None)
    retenciones_renta: float = field(metadata={"alias": "retencionesRenta"}, default=None)
    retenciones_renta_label: str = field(metadata={"alias": "retencionesRentaLabel"}, default=None)
    nro_pago1: str = field(metadata={"alias": "nroPago1"}, default=None)
    nro_pago2: str = field(metadata={"alias": "nroPago2"}, default=None)
    total_a_pagar: float = field(metadata={"alias": "totalapagar"}, default=None)
    total_aplicado: float = field(metadata={"alias": "totalaplicado"}, default=None)
    aplicado_a_este_pago: float = field(metadata={"alias": "aplicadoAEstePago"}, default=None)


class ComprasPagoDetailsRequest:
    def __init__(self, auth_user, auth_password, params_user, token, id_empresa, id_pago):
        self._auth_user = auth_user
        self._auth_password = auth_password
        self._params_user = params_user
        self._token = token
        self._id_pago = id_pago
        self._id_empresa = id_empresa

    def to_dict(self):
        return {
            "auth": {
                "usuario": self._auth_user,
                "password": self._auth_password
            },
            "service": {
                "provision": "Pago",
                "operacion": "leer_pago"
            },
            "parameters": {
                "sesion": {
                    "usuario": self._params_user,
                    "claveSesion": self._token
                },
                "idPago": self._id_pago,
                "idEmpresa": self._id_empresa
            }
        }


class ComprasPagoDetailsResponse:
    def __init__(self, response):
        self._response = response

    def get_pago_details(self):
        if not ColppyError(self._response).is_error():
            data = self._response['response']['data']
            return CompraPagoDetail(**data)
        return None
