import asyncio
from colppy.operations.main import ColppyAPIClient
from groovindb import GroovinDB
from db_types import GeneratedClient
from colppy.helpers.formatters import sql_bulk

async def main():
    db: GeneratedClient  = GroovinDB().client
    colppy_client = ColppyAPIClient()
    await colppy_client.get_token()
    await db.dev.execute('TRUNCATE TABLE norm_colppy.empresas RESTART IDENTITY;')
    empresas = await colppy_client.get_empresas()

    items = await colppy_client.get_empresas()
    query_empresas = sql_bulk(models=items, schema_db="norm_colppy", table_name="empresas")
    print(query_empresas)



    items = await colppy_client.get_all_movimientos()
    query_movimientos = sql_bulk(models=items, schema_db="norm_colppy", table_name="movimientos")
    print(query_movimientos)

    await db.dev.execute(query_movimientos)

    await colppy_client.logout()

if __name__ == "__main__":
    asyncio.run(main())
