from fastapi import APIRouter

from auth.api import auth_controller
from datafeed.api import datafeed_controller
from gdpr import gdpr_controller
from plugin.token.api import plugin_token_controller
from silent_request.api import (
    silent_request_controller,
)

router = APIRouter(prefix="/v1")

router.include_router(auth_controller.router)
router.include_router(plugin_token_controller.router)
router.include_router(silent_request_controller.router)
router.include_router(datafeed_controller.router)
router.include_router(gdpr_controller.router)
