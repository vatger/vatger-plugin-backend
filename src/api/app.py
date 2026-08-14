from fastapi import FastAPI

from api.router import main_router
from auth.api import auth_controller
from containers.dependencies import DependencyContainer
from datafeed.api import datafeed_controller
from gdpr import gdpr_controller
from plugin.token.api import plugin_token_controller
from silent_request.api import (
    silent_request_controller,
)

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
