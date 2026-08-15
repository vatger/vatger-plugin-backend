import uuid

from sqlalchemy.exc import IntegrityError

from containers.database import SessionFactory
from users.interfaces.user_repository_interface import (
    UserAlreadyExistsError,
    UserRepositoryInterface,
)
from users.user import User
from users.user_model import UserModel


class PostgresUserRepository(UserRepositoryInterface):
    def __init__(self, session_factory: SessionFactory):
        self.session_factory = session_factory

    def _to_domain(self, db_model: UserModel) -> User:
        return User(
            id=db_model.id,
            cid=db_model.cid,
            name=db_model.name,
            rating=db_model.rating,
            admin=db_model.admin,
            access=db_model.access,
        )

    def _to_sql(self, user: User) -> UserModel:
        return UserModel(
            id=user.id,
            cid=user.cid,
            name=user.name,
            rating=user.rating,
            admin=user.admin,
            access=user.access,
        )

    def get_user(self, id: uuid.UUID) -> User:
        with self.session_factory() as session:
            row = session.get(UserModel, id)
            return self._to_domain(row) if row else None

    def get_user_by_cid(self, cid: str) -> User | None:
        with self.session_factory() as session:
            row = session.query(UserModel).filter(UserModel.cid == cid).first()
            return self._to_domain(row) if row else None

    def add_user(self, user: User):
        with self.session_factory() as session:
            row = self._to_sql(user)
            session.add(row)
            try:
                session.commit()
            except IntegrityError as e:
                session.rollback()
                raise UserAlreadyExistsError(user.cid) from e
            return user

    def update_user(self, user: User):
        with self.session_factory() as session:
            row = session.get(UserModel, user.id)
            if not row:
                msg = f"user {user.id} not found"
                raise ValueError(msg)

            row.name = user.name
            row.rating = user.rating
            row.admin = user.admin
            row.access = user.access

            session.commit()
            return self._to_domain(row)

    def delete(self, id: uuid.UUID):
        with self.session_factory() as session:
            row = session.get(UserModel, id)
            if row:
                session.delete(row)
                session.commit()
