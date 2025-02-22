from typing import List, Dict, Callable
from fastapi import HTTPException
from pvmlib.database.database import DatabaseManager
from aiohttp import ClientSession
from urllib.parse import urlparse

class DependencyChecker:
    def __init__(self, dependencies: List[Callable[[], Dict[str, str]]]):
        self.dependencies = dependencies

    async def check_dependencies(self) -> Dict[str, str]:
        results = {}
        for check in self.dependencies:
            try:
                result = await check()
                results.update(result)
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Dependency check failed: {str(e)}")
        return results

async def check_mongo(database_manager: DatabaseManager) -> Dict[str, str]:
    try:
        # Verificar si ya hay una conexión existente
        if not database_manager.mongo_client:
            await database_manager.connect_to_mongo()
        
        await database_manager.mongo_database.command("ping")
        return {"mongodb": "UP"}
    except Exception as e:
        return {"mongodb": "DOWN"}

async def check_external_service(url: str) -> Dict[str, str]:
    try:
        async with ClientSession() as session:
            async with session.get(url) as response:
                parsed_url = urlparse(url)
                service_name = f"{parsed_url.hostname}{parsed_url.path.rsplit('/', 1)[0]}"
                if response.status == 200:
                    return {service_name: "UP"}
                else:
                    return {service_name: "DOWN"}
    except Exception as e:
        parsed_url = urlparse(url)
        service_name = f"{parsed_url.hostname}{parsed_url.path.rsplit('/', 1)[0]}"
        return {service_name: "DOWN"}
