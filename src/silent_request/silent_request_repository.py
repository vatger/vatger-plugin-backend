import uuid
from datetime import UTC

from sqlalchemy.exc import IntegrityError

from containers.database import SessionFactory
from silent_request.interfaces.silent_request_repository_interface import (
    DuplicateSilentRequestException,
    SilentRequestRepositoryInterface,
)
from silent_request.silent_request import SilentRequest
from silent_request.silent_request_model import SilentRequestModel


class PostgresSilentRequestRepository(SilentRequestRepositoryInterface):
    def __init__(self, session_factory: SessionFactory):
        self.session_factory = session_factory

    def _to_domain(self, db_model: SilentRequestModel) -> SilentRequest:
        return SilentRequest(
            id=db_model.id,
            callsign=db_model.callsign,
            user_id=db_model.user_id,
            departure_icao=db_model.departure_icao,
            type=db_model.type,
            requested_at=db_model.requested_at.replace(tzinfo=UTC),
        )

    def _to_sql(self, request: SilentRequest) -> SilentRequestModel:
        return SilentRequestModel(
            id=request.id,
            callsign=request.callsign,
            user_id=request.user_id,
            departure_icao=request.departure_icao,
            type=request.type,
            requested_at=request.requested_at.replace(tzinfo=UTC),
        )

    def create_request(self, request: SilentRequest) -> SilentRequest:
        with self.session_factory() as session:
            row = self._to_sql(request)
            session.add(row)
            try:
                session.commit()
            except IntegrityError as e:
                session.rollback()
                raise DuplicateSilentRequestException from e
            return request

    def get_request_by_callsign(self, callsign: str) -> SilentRequest | None:
        with self.session_factory() as session:
            row = (
                session
                .query(SilentRequestModel)
                .filter(SilentRequestModel.callsign == callsign)
                .first()
            )
            return self._to_domain(row) if row else None

    def get_request_by_user_id(self, id: uuid.UUID) -> SilentRequest | None:
        with self.session_factory() as session:
            row = session.query(SilentRequestModel).filter(SilentRequestModel.user_id == id).first()
            return self._to_domain(row) if row else None

    def get_requests_by_icao(self, icao: str) -> list[SilentRequest] | None:
        with self.session_factory() as session:
            rows = (
                session
                .query(SilentRequestModel)
                .filter(SilentRequestModel.departure_icao == icao)
                .all()
            )
            return [self._to_domain(row) for row in rows]

    def get_all_requests(self) -> list[SilentRequest] | None:
        with self.session_factory() as session:
            rows = session.query(SilentRequestModel).all()
            return [self._to_domain(row) for row in rows]

    def delete_request_by_callsign(self, callsign: str) -> bool:
        with self.session_factory() as session:
            row = (
                session
                .query(SilentRequestModel)
                .filter(SilentRequestModel.callsign == callsign)
                .first()
            )
            if row:
                session.delete(row)
                session.commit()
                return True
            return False

    def delete_request_by_user(self, user_id: uuid.UUID) -> bool:
        with self.session_factory() as session:
            row = (
                session
                .query(SilentRequestModel)
                .filter(SilentRequestModel.user_id == user_id)
                .first()
            )
            if row:
                session.delete(row)
                session.commit()
                return True
            return False
