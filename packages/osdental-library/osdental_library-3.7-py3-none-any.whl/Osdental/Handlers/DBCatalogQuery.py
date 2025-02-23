import os
from dotenv import load_dotenv
from typing import Dict
from Osdental.Database.Connection import Connection

load_dotenv()

class DBCatalogQuery:

    def __init__(self):
        self.db = Connection(os.getenv('DATABASE_CATALOG'))
    
    async def get_data_catalog(self, catalog_name:str) -> Dict[str,str]:
        rows = await self.db.execute_query_return_data('EXEC CATALOG.sps_GetCatalogByName @i_nameCatalog = :catalog_name', {'catalog_name': catalog_name})
        return {
            row.get('name'): row.get('value') for row in rows if row.get('value')
        }