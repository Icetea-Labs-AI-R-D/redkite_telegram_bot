from fastapi import FastAPI
import logging
import uvicorn
from routers import call_routes
from config.settings import settings
from config.database import init_mongo

logger = logging.getLogger(__name__)


async def lifespan(app: FastAPI):
    logger.info("Starting the application.")
    await init_mongo()
    yield
    logger.info("Stopping the application.")

app: FastAPI = FastAPI(
    title="Call Center",
    description="A simple call center API",
    version="0.1",
    openapi_url="/api/v1/openapi.json",
    docs_url="/api/v1/docs",
    redoc_url="/api/v1/redoc",
    lifespan=lifespan,
)

app.include_router(call_routes, prefix="")
if __name__ == "__main__":
    uvicorn.run("__main__:app", host="0.0.0.0", port=settings.PORT, timeout_keep_alive=30, reload=True, log_config="log_conf.yaml")
