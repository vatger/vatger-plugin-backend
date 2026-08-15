from typing import Annotated

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends

from api.guards import get_user
from containers.dependencies import DependencyContainer
from datafeed.api.datafeed_responses import ControllerResponse, PilotResponse
from interfaces.repositories.datafeed_repository_interface import DatafeedRepositoryInterface
from users.user import User

router = APIRouter(prefix="/datafeed", tags=["Datafeed"])


@router.get("/user/pilot", response_model=PilotResponse | None)
@inject
async def get_user_pilot_data(
    user: Annotated[User, Depends(get_user)],
    datafeed_repo: Annotated[
        DatafeedRepositoryInterface,
        Depends(Provide[DependencyContainer.datafeed_container.datafeed_repository]),
    ],
):
    pilot_data = await datafeed_repo.get_pilot_by_cid(int(user.cid))

    if not pilot_data:
        return

    return PilotResponse(**pilot_data.model_dump())


@router.get("/user/controller", response_model=ControllerResponse | None)
@inject
async def get_user_controller_data(
    user: Annotated[User, Depends(get_user)],
    datafeed_repo: Annotated[
        DatafeedRepositoryInterface,
        Depends(Provide[DependencyContainer.datafeed_container.datafeed_repository]),
    ],
):
    controller_data = await datafeed_repo.get_controller_by_cid(int(user.cid))

    if not controller_data:
        return

    return ControllerResponse(**controller_data.model_dump())
