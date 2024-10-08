#!/usr/bin/env python3
""" Database for sqlalchemy ORM """
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound
from user import Base, User


class DB:
    """ DB Class for Object Reational Mapping """

    def __init__(self):
        """ Constructor Method """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self):
        """ Session Getter Method """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """ A method that adds a user to the database
        return:
             User  Object"""
        user = User(email=email, hashed_password=hashed_password)
        self._session.add(user)
        self._session.commit()

        return user

    def find_user_by(self, **kwargs) -> User:
        """ Find the first user that
        matches the provided keyword arguments.

        Args:
            **kwargs: Arbitrary keyword arguments
            to filter the query.

        Returns:
            The first user row that matches the query.

        Raises:
            NoResultFound: If no user matches the query.
            InvalidRequestError: If an invalid query
            argument is passed.
            """
        if not kwargs:
            raise InvalidRequestError

        calumn_names = User.__table__.columns.keys()
        for key in kwargs.keys():
            if key not in calumn_names:
                raise InvalidRequestError

        try:
            user = self._session.query(User).filter_by(**kwargs).one()
            return user
        except NoResultFound:
            raise NoResultFound

    def update_user(self, user_id: int, **kwargs) -> None:
        """ Update the user's attributes
        based on the provided keyword arguments.

        Args:
            user_id (int): The ID of the user to update.
            **kwargs: Arbitrary keyword arguments
            representing user attributes to update.

        Returns:
            None

        Raises:
            ValueError: If an argument does
            not correspond to a user attribute.
            """
        try:
            user = self.find_user_by(id=user_id)
        except NoResultFound:
            raise ValueError

        valid_columns = User.__table__.columns.keys()

        for key, value in kwargs.items():
            if key not in valid_columns:
                raise ValueError
            setattr(user, key, value)

        self._session.commit()
