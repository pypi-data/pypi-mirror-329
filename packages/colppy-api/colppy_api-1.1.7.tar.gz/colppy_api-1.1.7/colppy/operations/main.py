import os
import json

import httpx

from colppy.helpers.logger import logger
from colppy.models.auth import LoginRequest, LoginResponse, LogoutRequest, LogoutResponse
from colppy.models.cobro_factura import CobroFacturaResponse, CobroFacturaRequest, CobroFactura
from colppy.models.compras_pago_details import ComprasPagoDetailsRequest, ComprasPagoDetailsResponse
from colppy.models.comprobante_compra_details import ComprobanteCompraDetailsRequest, ComprobanteCompraDetailsResponse, ComprobanteCompraDetails
from colppy.models.comprobante_venta_details import ComprobateVentaDetailsRequest, ComprobanteVentaDetailsResponse, ComprobanteVentaDetails
from colppy.models.comprobantes_compra import ComprobanteCompraRequest, ComprobanteCompraResponse, ComprobanteCompra
from colppy.models.comprobantes_venta import ComprobanteVentaRequest, ComprobanteVentaResponse, ComprobanteVenta
from colppy.models.movimientos import MovimientosRequest, MovimientosResponse, Movimiento

from colppy.models.response import Response
from colppy.models.empresas import EmpresasRequest, Empresa, EmpresasResponse
from colppy.models.clientes import ClientesRequest, Cliente, ClientesResponse
from colppy.models.proveedores import ProveedoresRequest, Proveedor, ProveedoresResponse


def get_config():
    try:
        config_path = os.path.join(os.getcwd(), 'config.json')
        with open(config_path) as config_file:
            return json.load(config_file)
    except FileNotFoundError:
        raise FileNotFoundError(
            "No se encontró el archivo config.json en el directorio raíz. "
            "Por favor, crea un archivo config.json en el directorio donde estás ejecutando tu aplicación."
        )


class ColppyAPIClient:
    def __init__(self):
        config = get_config()
        self._base_url = config['ColppyAPI']['COLPPY_API_URI']
        self._auth_user = config['ColppyAPI']['COLPPY_AUTH_USER']
        self._auth_password = config['ColppyAPI']['COLPPY_AUTH_PASSWORD']
        self._params_user = config['ColppyAPI']['COLPPY_PARAMS_USER']
        self._params_password = config['ColppyAPI']['COLPPY_PARAMS_PASSWORD']
        self._client = httpx.Client()
        self._token = None

    async def get_token(self) -> str or None:
        login_request = LoginRequest(
            auth_user=self._auth_user,
            auth_password=self._auth_password,
            params_user=self._params_user,
            params_password=self._params_password
        )

        async with httpx.AsyncClient(timeout=30.0) as client:
            try:
                response = await client.post(self._base_url, json=login_request.to_dict())
                response.raise_for_status()
                login_response = LoginResponse(response.json())
                self._token = login_response.get_token()
                logger.debug(f"Token: {self._token}")
                return login_response.get_token()
            except httpx.HTTPStatusError as e:
                logger.error(f"Error getting token: {e}")
                return None

    async def request_items_paginated(self, request, response_class):
        ret: list = []
        items = await self.request_items(request, response_class)
        while items:
            ret.extend(items)
            request.next_page()
            items = await self.request_items(request, response_class)

        logger.debug(f"REQUEST: Se consiguio una respuesta de {response_class} con {len(ret)} items")
        return ret

    async def request_items(self, request, response_class):
        async with httpx.AsyncClient(timeout=30.0) as client:
            try:
                response = await client.post(self._base_url, json=request.to_dict())
                response.raise_for_status()

                response = response_class(response.json())
                return response.get_items()

            except httpx.HTTPStatusError as e:
                logger.error(f"Error getting objects: {e}")
                return []

    async def get_empresas(self, filters=None, start=0, limit=10) -> list[Empresa]:
        empresas_request = EmpresasRequest(
            auth_user=self._auth_user,
            auth_password=self._auth_password,
            params_user=self._params_user,
            filters=filters,
            token=self._token
        )

        empresas = await self.request_items(empresas_request, EmpresasResponse)

        return [empresa for empresa in empresas if empresa.id_empresa != 11675]

    async def get_all_clientes(self) -> list[Cliente]:
        ret: list[Cliente] = []
        empresas = await self.get_empresas()
        for empresa in empresas:
            ret += await self.get_clientes_by_empresa(empresa)
        return ret

    async def get_clientes_by_empresa(self, empresa: Empresa) -> list[Cliente]:
        clientes_request = ClientesRequest(
            auth_user=self._auth_user,
            auth_password=self._auth_password,
            params_user=self._params_user,
            token=self._token,
            id_empresa=empresa.id_empresa,
            only_active=True,
        )

        return await self.request_items_paginated(clientes_request, ClientesResponse)

    async def get_all_proveedores(self) -> list[Proveedor]:
        ret: list[Proveedor] = []
        empresas = await self.get_empresas()
        for empresa in empresas:
            ret += await self.get_proveedores_by_empresa(empresa)
        return ret

    async def get_proveedores_by_empresa(self, empresa: Empresa) -> list[Proveedor]:
        proveedores_request = ProveedoresRequest(
            auth_user=self._auth_user,
            auth_password=self._auth_password,
            params_user=self._params_user,
            token=self._token,
            id_empresa=empresa.id_empresa
        )

        return await self.request_items_paginated(proveedores_request, ProveedoresResponse)

    async def get_all_movimientos(self) -> list[Movimiento]:
        ret: list[Movimiento] = []
        empresas = await self.get_empresas()
        for empresa in empresas:
            ret += await self.get_movimientos_by_empresa(empresa, from_date="2010-01-01", to_date="2040-01-01")
        return ret

    async def get_movimientos_by_empresa(self, empresa: Empresa, from_date="2013-01-01", to_date="2040-01-01") -> list[Proveedor]:
        movimientos_request = MovimientosRequest(
            auth_user=self._auth_user,
            auth_password=self._auth_password,
            params_user=self._params_user,
            token=self._token,
            id_empresa=empresa.id_empresa,
            from_date=from_date,
            to_date=to_date
        )

        return await self.request_items_paginated(movimientos_request, MovimientosResponse)

    ####################### METODOS VIEJOS #########################

    async def get_all_comprobantes_compra(self) -> list[ComprobanteCompra]:
        ret: list[ComprobanteCompra] = []
        empresas = await self.get_empresas()
        for empresa in empresas:
            ret += await self.get_comprobantes_compras_by_empresa(empresa)
        return ret

    async def get_comprobantes_compras_by_empresa(self, empresa: Empresa, id_tipo_comprobante=None, filters=None,
                                                  start=0,
                                                  limit=100):
        comprobantes_compra_request = ComprobanteCompraRequest(
            auth_user=self._auth_user,
            auth_password=self._auth_password,
            params_user=self._params_user,
            token=self._token,
            id_empresa=empresa.id_empresa,
            id_tipo_comprobante=id_tipo_comprobante,
            filters=filters,
            start=start,
            limit=limit
        )

        async with httpx.AsyncClient(timeout=30.0) as client:
            try:
                response = await client.post(self._base_url, json=comprobantes_compra_request.to_dict(), timeout=240)
                response.raise_for_status()
                comprobantes_compra_response = ComprobanteCompraResponse(response.json())
                logger.debug(f"Comprobantes de compra de la empresa {empresa.nombre} (id: {empresa.id_empresa}): {len(comprobantes_compra_response.get_comprobantes())}")
                return comprobantes_compra_response.get_comprobantes()
            except httpx.HTTPStatusError as e:
                logger.error(f"Error getting comprobantes de compra: {e}")
                return []

    async def get_all_comprobantes_venta(self) -> list[ComprobanteVenta]:
        ret: list[ComprobanteVenta] = []
        empresas = await self.get_empresas()
        for empresa in empresas:
            ret += await self.get_comprobantes_ventas_by_empresa(empresa)
        return ret

    async def get_comprobantes_ventas_by_empresa(self, empresa: Empresa, id_tipo_comprobante=None, filters=None,
                                                 start=0,
                                                 limit=100):
        comprobantes_venta_request = ComprobanteVentaRequest(
            auth_user=self._auth_user,
            auth_password=self._auth_password,
            params_user=self._params_user,
            token=self._token,
            id_empresa=empresa.id_empresa,
            id_tipo_comprobante=id_tipo_comprobante,
            filters=filters,
            start=start,
            limit=limit
        )

        async with httpx.AsyncClient(timeout=30.0) as client:
            try:
                response = await client.post(self._base_url, json=comprobantes_venta_request.to_dict(), timeout=240)
                response.raise_for_status()
                comprobantes_venta_response = ComprobanteVentaResponse(response.json())
                logger.debug(f"Comprobantes de venta de la empresa {empresa.nombre} (id: {empresa.id_empresa}): {len(comprobantes_venta_response.get_comprobantes())}")
                return comprobantes_venta_response.get_comprobantes()
            except httpx.HTTPStatusError as e:
                logger.error(f"Error getting comprobantes de venta: {e}")
                return []

    async def get_all_comprobante_compra_details_by_id(self, start=0, limit=50) -> list[ComprobanteCompraDetails]:
        ret: list[ComprobanteCompraDetails] = []
        empresas = await self.get_empresas()
        for empresa in empresas:
            comprobantes_empresa = await self.get_comprobantes_compras_by_empresa(empresa)
            for comprobante in comprobantes_empresa:
                ret += await self.get_comprobante_compra_details_by_id(empresa, comprobante.id_factura)
        return ret

    async def get_comprobante_compra_details_by_id(self, empresa: Empresa, id_comprobante):
        comprobante_details_request = ComprobanteCompraDetailsRequest(
            auth_user=self._auth_user,
            auth_password=self._auth_password,
            params_user=self._params_user,
            token=self._token,
            id_empresa=empresa.id_empresa,
            id_comprobante=id_comprobante
        )

        async with httpx.AsyncClient(timeout=30.0) as client:
            try:
                response = await client.post(self._base_url, json=comprobante_details_request.to_dict())
                response.raise_for_status()
                comprobante_details_response = ComprobanteCompraDetailsResponse(response.json())
                return comprobante_details_response.get_comprobante()
            except httpx.HTTPStatusError as e:
                logger.error(f"Error getting comprobante details: {e}")
                return None

    async def get_all_comprobante_venta_details_by_id(self, start=0, limit=50) -> list[ComprobanteVentaDetails]:
        ret: list[ComprobanteVentaDetails] = []
        empresas = await self.get_empresas()
        for empresa in empresas:
            comprobantes_empresa= await self.get_comprobantes_ventas_by_empresa(empresa)
            for comprobante in comprobantes_empresa:
                ret += await self.get_comprobante_venta_details_by_id(empresa, comprobante.id_factura)
        return ret

    async def get_comprobante_venta_details_by_id(self, empresa: Empresa, id_comprobante):
        comprobante_details_request = ComprobateVentaDetailsRequest(
            auth_user=self._auth_user,
            auth_password=self._auth_password,
            params_user=self._params_user,
            token=self._token,
            id_empresa=empresa.id_empresa,
            id_comprobante=id_comprobante
        )

        async with httpx.AsyncClient(timeout=30.0) as client:
            try:
                response = await client.post(self._base_url, json=comprobante_details_request.to_dict())
                response.raise_for_status()
                comprobante_details_response = ComprobanteVentaDetailsResponse(response.json())
                return comprobante_details_response.get_comprobante()
            except httpx.HTTPStatusError as e:
                logger.error(f"Error getting comprobante details: {e}")
                return None

    async def get_all_cobro_factura(self, start=0, limit=50) -> list[CobroFactura]:
        ret: list[CobroFactura] = []
        empresas = await self.get_empresas()
        for empresa in empresas:
            comprobantes_empresa = await self.get_comprobantes_compras_by_empresa(empresa)
            for comprobante in comprobantes_empresa:
                ret += await self.get_cobro_factura_by_id(empresa, comprobante.id_factura)
        return ret

    async def get_cobro_factura_by_id(self, empresa: Empresa, id_factura) -> list[CobroFactura]:
        cobro_factura_request = CobroFacturaRequest(
            auth_user=self._auth_user,
            auth_password=self._auth_password,
            params_user=self._params_user,
            token=self._token,
            id_empresa=empresa.id_empresa,
            id_factura=id_factura
        )

        async with httpx.AsyncClient(timeout=30.0) as client:
            try:
                response = await client.post(self._base_url, json=cobro_factura_request.to_dict())
                response.raise_for_status()
                cobro_factura_response = CobroFacturaResponse(response.json())
                return cobro_factura_response.get_cobro()
            except httpx.HTTPStatusError as e:
                logger.error(f"Error getting cobro factura: {e}")
                return []

    async def get_compras_pago_details_by_id_batch(self, id_pagos, empresa: Empresa):
        import pandas as pd
        all_pago_details = pd.DataFrame()

        async with httpx.AsyncClient(timeout=30.0) as client:
            for id_pago in id_pagos:
                compras_pago_request = ComprasPagoDetailsRequest(
                    auth_user=self._auth_user,
                    auth_password=self._auth_password,
                    params_user=self._params_user,
                    token=self._token,
                    id_pago=id_pago,
                    id_empresa=empresa.id_empresa
                )

                try:
                    response = await client.post(self._base_url, json=compras_pago_request.to_dict(), timeout=240)
                    response.raise_for_status()
                    compras_pago_response = ComprasPagoDetailsResponse(response.json())
                    logger.debug(
                        f"Detalles del pago {id_pago} para la empresa:{empresa}: {compras_pago_response.get_pago_details().to_dataframe()}")
                    pago_details = compras_pago_response.get_pago_details().to_dataframe()

                    if not pago_details.empty:
                        all_pago_details = pd.concat([all_pago_details, pago_details], ignore_index=True)
                except httpx.HTTPStatusError as e:
                    logger.error(f"Error al obtener detalles del pago {id_pago}: {e}")
                    continue

        return all_pago_details

    async def logout(self):
        logout_request = LogoutRequest(
            auth_user=self._auth_user,
            auth_password=self._auth_password,
            params_user=self._params_user,
            token=self._token
        )

        async with httpx.AsyncClient(timeout=30.0) as client:
            try:
                response = await client.post(self._base_url, json=logout_request.to_dict())
                response.raise_for_status()
                logout_response = LogoutResponse(response.json())
                logger.debug(f"Logout: {logout_response.get_logout()}")
                return logout_response.get_logout()
            except httpx.HTTPStatusError as e:
                logger.error(f"Error logging out: {e}")
                return False
