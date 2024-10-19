from fastapi import APIRouter
from .whatsapp_routes import router as whatsapp_router
from .messenger_routes import router as messenger_router
from .telegram_routes import router as telegram_router
from .instagram_routes import router as instagram_router
from .custom_routes import router as custom_router
from .scala360_routes import router as scala360_router

router = APIRouter(prefix="/api")
router.include_router(whatsapp_router, prefix="/whatsapp", tags=["whatsapp"])
router.include_router(messenger_router, prefix="/messenger", tags=["messenger"])
router.include_router(telegram_router, prefix="/telegram", tags=["telegram"])
router.include_router(instagram_router, prefix="/instagram", tags=["instagram"])
router.include_router(custom_router, prefix="/custom", tags=["custom"])
router.include_router(scala360_router, prefix="/scala360", tags=["scala360"])
