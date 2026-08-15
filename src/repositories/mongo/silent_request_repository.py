import uuid
from datetime import UTC

from pymongo.collection import Collection
from pymongo.errors import DuplicateKeyError

from silent_request.interfaces.silent_request_repository_interface import (
    DuplicateSilentRequestException,
    SilentRequestRepositoryInterface,
)
from silent_request.silent_request import SilentRequest


class MongoSilentRequestRepository(SilentRequestRepositoryInterface):
    def __init__(self, collection: Collection):
        self.collection = collection

        self.collection.create_index("callsign", unique=True)
        self.collection.create_index("user_id", unique=True)

    def _doc_to_request(self, doc: dict) -> SilentRequest:
        return SilentRequest(
            callsign=doc["callsign"],
            user_id=uuid.UUID(doc["user_id"]),
            departure_icao=doc["departure_icao"],
            type=doc["type"],
            requested_at=doc["requested_at"].replace(tzinfo=UTC),
        )

    def _request_to_doc(self, request: SilentRequest) -> dict:
        return {
            "callsign": request.callsign,
            "user_id": str(request.user_id),
            "departure_icao": request.departure_icao,
            "type": request.type,
            "requested_at": request.requested_at,
        }

    def create_request(self, request: SilentRequest) -> SilentRequest:
        try:
            self.collection.insert_one(self._request_to_doc(request))
        except DuplicateKeyError:
            raise DuplicateSilentRequestException from None
        else:
            return request

    def get_request_by_callsign(self, callsign: str) -> SilentRequest | None:
        doc = self.collection.find_one({"callsign": callsign})

        if not doc:
            return None

        return self._doc_to_request(doc)

    def get_request_by_user_id(self, id: uuid.UUID) -> SilentRequest | None:
        doc = self.collection.find_one({"user_id": str(id)})

        if not doc:
            return None

        return self._doc_to_request(doc)

    def get_requests_by_icao(self, icao: str) -> list[SilentRequest] | None:
        results = [
            self._doc_to_request(doc) for doc in self.collection.find({"departure_icao": icao})
        ]

        return results or None

    def get_all_requests(self) -> list[SilentRequest] | None:
        docs = self.collection.find()

        if not docs:
            return None

        return [request for doc in docs if (request := self._doc_to_request(doc)) is not None]

    def delete_request_by_callsign(self, callsign: str) -> bool:
        result = self.collection.delete_one({"callsign": callsign})
        return result.deleted_count == 1

    def delete_request_by_user(self, user_id: uuid.UUID) -> bool:
        result = self.collection.delete_one({"user_id": str(user_id)})
        return result.deleted_count == 1
