import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.health import router as health_router
from app.api.health_db import router as health_db_router
from app.core.config import settings
from app.core.logging import setup_logging

setup_logging()
logger = logging.getLogger(__name__)

# Using lifespan for startup/shutdown events, which is more flexible and test-friendly than the 
# older on_event approach
# def create_app() -> FastAPI:
#     app = FastAPI(title=settings.app_name)

#     app.include_router(health_router)

#     @app.on_event("startup")
#     def on_startup():
#         logger.info("Starting app", extra={"environment": settings.environment})

#     return app

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic: runs before the app starts receiving requests
    logger.info("Starting app", extra={"environment": settings.environment})
    yield
    # Shutdown logic: runs after the app finishes handling requests
    logger.info("Shutting down app")

def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.app_name,
        lifespan=lifespan  # Hook the lifespan manager here
    )
    app.include_router(health_router)
    app.include_router(health_db_router)
    return app

app = create_app()


"""
EXAMPLE OF USING LIFESPAN TO MANAGE A SHARED RESOURCE (e.g., DB CONNECTION POOL)

from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, Request

# 1. THE LIFESPAN (Global Setup)
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Create the expensive resource once
    app.state.db_pool = await create_db_pool() 
    yield
    # Shutdown: Clean it up once
    await app.state.db_pool.close()

# 2. THE DEPENDENCY (The Hand-off)
def get_db(request: Request):
    # Grabs the pool we attached to the app state
    return request.app.state.db_pool

app = FastAPI(lifespan=lifespan)

# 3. THE ROUTE (The Usage)
@app.get("/items")
async def read_items(db = Depends(get_db)):
    # Use the connection already waiting in the pool
    return await db.fetch("SELECT * FROM items")


Why this is better than Middleware
Startup Logic: The database pool is created only once when the server starts.
Dependency Logic: The get_db function only runs for routes that actually need the database.
 Middleware would force every single request—even static files or health checks—to 
 interact with your database logic unnecessarily.
Clean Teardown: When the server stops, the lifespan ensures 
all connections are closed properly, 
preventing "leaked" or orphaned connections. 
Medium
Medium
 +5
Common Use Cases for Lifespan 
Reddit
Reddit
Connection Pools: Database (SQLAlchemy, Motor, asyncpg) and Redis.
Heavy Models: Loading 1GB+ Machine Learning models into GPU memory.
Shared Clients: Initializing a single httpx.AsyncClient to reuse for all outgoing API calls. 

"""