from fastapi import FastAPI
from mangum import Mangum
from app.routes.health import router as health_router
from app.routes.order import router as order_router
from app.exceptions.handlers import add_global_error_handler
from app.routes.payment import router as payment_router
from app.config.config import Base, init_db
from app.middleware.alb_auth import ALBCognitoAuth
from fastapi import Request
import logging

# this import are create database entities before start the application
from app.entity.order_entity import Order
from app.entity.order_entries import OrderEntry

app = FastAPI()
security = ALBCognitoAuth()
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

@app.on_event("startup")
async def startup_event():
    logger.info("🚀 App startup initiated.")
    engine = init_db()
    Base.metadata.create_all(bind=engine)
    logger.info("🚀 App startup end.")


@app.middleware("http")
async def auth_middleware(request: Request, call_next):
    if request.url.path in ["/health", "/public"]:
        request.state.skip_auth = True
    return await call_next(request)

# Add global error handler
add_global_error_handler(app)

# Include routers
app.include_router(health_router)
app.include_router(order_router)
app.include_router(payment_router)

# Lambda handler
handler = Mangum(app)