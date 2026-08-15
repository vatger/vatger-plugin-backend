import uuid

from sqlalchemy.exc import IntegrityError

from containers.database import SessionFactory
from plugin.token.interfaces.plugin_token_repository_interface import PluginTokenRepositoryInterface
from plugin.token.plugin_token import PluginToken
from plugin.token.plugin_token_model import PluginTokenModel


class PostgresPluginTokenRepository(PluginTokenRepositoryInterface):
    def __init__(self, session_factory: SessionFactory):
        self.session_factory = session_factory

    def _to_domain(self, db_model: PluginTokenModel) -> PluginToken:
        return PluginToken(
            id=db_model.id,
            user=db_model.user,
            label=db_model.label,
            polling_secret=db_model.polling_secret,
            token=db_model.token,
            last_used=db_model.last_used,
        )

    def _to_sql(self, domain_model: PluginToken) -> PluginTokenModel:
        return PluginTokenModel(
            id=domain_model.id,
            user=domain_model.user,
            label=domain_model.label,
            polling_secret=domain_model.polling_secret,
            token=domain_model.token,
            last_used=domain_model.last_used,
        )

    def create(self, token: PluginToken) -> PluginToken:
        with self.session_factory() as session:
            row = self._to_sql(token)
            session.add(row)
            try:
                session.commit()
            except IntegrityError as e:
                session.rollback()
                msg = f"Token with id {token.id} or token value already exists"
                raise ValueError(msg) from e
            return token

    def get(self, id: uuid.UUID) -> PluginToken | None:
        with self.session_factory() as session:
            row = session.get(PluginTokenModel, id)
            return self._to_domain(row) if row else None

    def get_by_token(self, token: str) -> PluginToken | None:
        with self.session_factory() as session:
            row = (
                session
                .query(PluginTokenModel)
                .filter(PluginTokenModel.token == token)
                .one_or_none()
            )
            return self._to_domain(row) if row else None

    def get_tokens(self) -> list[PluginToken]:
        with self.session_factory() as session:
            rows = session.query(PluginTokenModel).all()
            return [self._to_domain(row) for row in rows]

    def get_tokens_by_user(self, user_id: uuid.UUID) -> list[PluginToken]:
        with self.session_factory() as session:
            rows = session.query(PluginTokenModel).filter(PluginTokenModel.user == user_id).all()
            return [self._to_domain(row) for row in rows]

    def update(self, token: PluginToken) -> PluginToken | None:
        with self.session_factory() as session:
            row = session.get(PluginTokenModel, token.id)
            if not row:
                msg = f"Token {token.id} not found"
                raise ValueError(msg)

            # TODO: what'S the best way to update?
            row.user = token.user
            row.label = token.label
            row.polling_secret = token.polling_secret
            row.token = token.token
            row.last_used = token.last_used

            session.commit()
            return self._to_domain(row)

    def delete(self, id: uuid.UUID) -> bool:
        with self.session_factory() as session:
            row = session.get(PluginTokenModel, id)
            if row:
                session.delete(row)
                session.commit()
                return True
            return False
