import os
from fastapi import APIRouter
from pvmlib.schemas.healthcheck_reponse_schema import responses_readiness, ReadinessResponse
from pvmlib.utils.dependecy_check import DependencyChecker, check_mongo, check_external_service
from pvmlib.database.database import DatabaseManager

readiness_router = APIRouter()
database_manager = DatabaseManager()

dependency_services = os.getenv("SERVICES_DEPENDENCY_HEALTHCHECK", "").split(",") 

@readiness_router.get(
    "/healthcheck/readness", 
    tags=["Health Check"], 
    responses=responses_readiness, 
    summary="Status de los recursos",
    response_model=ReadinessResponse
)
async def readiness() -> ReadinessResponse:
    """ Comprueba que el servicio este operando """
    dependencies = []

    if dependency_services and any(dependency_services):
        dependencies.extend([lambda url=url: check_external_service(url) for url in dependency_services if url])

    if database_manager.mongo_client:
        dependencies.append(lambda: check_mongo(database_manager))

    if not dependencies:
        return ReadinessResponse(
            status="ready",
            code=200,
            dependencies={}
        )

    checker = DependencyChecker(dependencies=dependencies)
    dependencies_status = await checker.check_dependencies()

    return ReadinessResponse(
        status="ready" if all(status == "UP" for status in dependencies_status.values()) else "not ready",
        code=200 if all(status == "UP" for status in dependencies_status.values()) else 500,
        dependencies=dependencies_status
    )