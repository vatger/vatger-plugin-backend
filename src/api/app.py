from fastapi import FastAPI

from api.router import main_router
from api.v1 import (
    auth_controller,
    datafeed_controller,
    silent_request_controller,
)
from containers.dependencies import DependencyContainer
from gdpr import gdpr_controller
from plugin.token.api import plugin_token_controller

app = FastAPI()
app.include_router(main_router)

container = DependencyContainer()
container.wire(
    modules=[
        auth_controller,
        plugin_token_controller,
        silent_request_controller,
        datafeed_controller,
        gdpr_controller,
    ]
)
