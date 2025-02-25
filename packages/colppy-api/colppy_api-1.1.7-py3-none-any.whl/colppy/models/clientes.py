from dataclasses import dataclass, field
from datetime import datetime

from colppy.helpers.errors import ColppyError
from colppy.helpers.formatters import BaseModel
from colppy.models.request import Request
from colppy.models.response import Response


@dataclass(init=False)
class Cliente(BaseModel):
    id_cliente: int = field(metadata={"alias": "idCliente", "field_name": "id_colppy", "unique": True}, default=None)
    razon_social: str = field(metadata={"alias": "RazonSocial"}, default=None)
    nombre_fantasia: str = field(metadata={"alias": "NombreFantasia"}, default=None)
    fecha_alta: datetime = field(metadata={"alias": "FechaAlta"}, default=None)
    dir_postal: str = field(metadata={"alias": "DirPostal"}, default=None)
    dir_postal_ciudad: str = field(metadata={"alias": "DirPostalCiudad"}, default=None)
    dir_postal_codigo_postal: str = field(metadata={"alias": "DirPostalCodigoPostal"}, default=None)
    dir_postal_provincia: str = field(metadata={"alias": "DirPostalProvincia"}, default=None)
    dir_postal_pais: str = field(metadata={"alias": "DirPostalPais"}, default=None)
    dir_fiscal: str = field(metadata={"alias": "DirFiscal"}, default=None)
    dir_fiscal_ciudad: str = field(metadata={"alias": "DirFiscalCiudad"}, default=None)
    dir_fiscal_codigo_postal: str = field(metadata={"alias": "DirFiscalCodigoPostal"}, default=None)
    dir_fiscal_provincia: str = field(metadata={"alias": "DirFiscalProvincia"}, default=None)
    dir_fiscal_pais: str = field(metadata={"alias": "DirFiscalPais"}, default=None)
    telefono: str = field(metadata={"alias": "Telefono", "to_sql": False}, default=None)
    fax: str = field(metadata={"alias": "Fax", "to_sql": False}, default=None)
    activo: int = field(metadata={"alias": "Activo", "to_sql": False}, default=0)
    #activo: int = field(metadata={"alias": "Activo"}, default=0)
    limite_credito: float = field(metadata={"alias": "LimiteCredito", "to_sql": False}, default=0.0)
    id_condicion_pago: int = field(metadata={"alias": "IdCondicionPago"}, default=0)
    id_condicion_iva: int = field(metadata={"alias": "IdCondicionIVA"}, default=0)
    cuit: str = field(metadata={"alias": "CUIT"}, default=None)
    producto: str = field(metadata={"alias": "Producto"}, default=None)
    id_tipo_percepcion: int = field(metadata={"alias": "IdTipoPercepcion", "to_sql": False}, default=0)
    certificado_exclusion: str = field(metadata={"alias": "CertificadoExclusion", "to_sql": False}, default=None)
    id_plan_cuenta: int = field(metadata={"alias": "IdPlanCuenta", "to_sql": False}, default=0)
    nro_cuenta: str = field(metadata={"alias": "NroCuenta", "to_sql": False}, default=None)
    cbu: str = field(metadata={"alias": "CBU", "to_sql": False}, default=None)
    banco: str = field(metadata={"alias": "Banco", "to_sql": False}, default=None)
    des_banco: str = field(metadata={"alias": "DesBanco", "to_sql": False}, default=None)
    porcentaje_iva: float = field(metadata={"alias": "PorcentajeIVA"}, default=0.0)
    porcentaje_desc: float = field(metadata={"alias": "PorcentajeDesc", "to_sql": False}, default=0.0)
    id_ret_ganancias: int = field(metadata={"alias": "IdRetGanancias", "to_sql": False}, default=0)
    email: str = field(metadata={"alias": "Email"}, default=None)
    dni: str = field(metadata={"alias": "DNI", "to_sql": False}, default=None)
    country_id: int = field(metadata={"alias": "CountryId"}, default=0)
    record_insert_ts: str = field(metadata={"alias": "RecordInsertTS", "to_sql": False}, default=None)
    record_update_ts: str = field(metadata={"alias": "RecordUpdateTS", "to_sql": False}, default=None)
    saldo: float = field(metadata={"alias": "Saldo"}, default=0.0)


class ClientesRequest(Request):
    def __init__(self, auth_user, auth_password, params_user, token, id_empresa,
                 only_active=True, page_size=50):
        super().__init__(page_size)
        self._auth_user = auth_user
        self._auth_password = auth_password
        self._params_user = params_user
        self._id_empresa = id_empresa
        self._only_active = only_active
        self._filters = []
        self._token = token

    def to_dict(self):
        if self._only_active:
            self._filters.append({
                "field": "Activo",
                "op": "=",
                "value": "1"
            })

        return {
            "auth": {
                "usuario": self._auth_user,
                "password": self._auth_password
            },
            "service": {
                "provision": "Cliente",
                "operacion": "listar_cliente"
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
                "order": [
                    {
                        "field": "NombreFantasia",
                        "dir": "asc"
                    }
                ]
            }
        }

class ClientesResponse(Response):
    def __init__(self, http_response):
        super().__init__(Cliente, http_response)