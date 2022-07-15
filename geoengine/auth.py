'''
Module for encapsulating Geo Engine authentication
'''

from typing import ClassVar, Dict, Optional, Tuple
from uuid import UUID

import os
from dotenv import load_dotenv
import requests as req
from requests.auth import AuthBase

from geoengine.error import GeoEngineException, UninitializedException


class BearerAuth(AuthBase):  # pylint: disable=too-few-public-methods
    '''A bearer token authentication for `requests`'''

    __token: str

    def __init__(self, token: str):
        self.__token = token

    def __call__(self, r):
        r.headers['Authorization'] = f'Bearer {self.__token}'
        return r


class Session:
    '''
    A Geo Engine session
    '''

    __id: UUID
    __valid_until: Optional[str] = None
    __server_url: str

    session: ClassVar[req.Session] = None

    def __init__(self, server_url: str, credentials: Tuple[str, str] = None, token: str = None) -> None:
        '''
        Initialize communication between this library and a Geo Engine instance

        If credentials or a token are provided, the session will be authenticated.
        Credentials and token must not be provided at the same time.

        optional arguments: (email, password) as tuple or token as a string
        optional environment variables: GEOENGINE_EMAIL, GEOENGINE_PASSWORD, GEOENGINE_TOKEN
        '''

        session = None

        if credentials is not None and token is not None:
            raise GeoEngineException('Cannot provide both credentials and token')

        if credentials is not None:
            session = req.post(f'{server_url}/login', json={"email": credentials[0], "password": credentials[1]}).json()
        elif "GEOENGINE_EMAIL" in os.environ and "GEOENGINE_PASSWORD" in os.environ:
            session = req.post(f'{server_url}/login',
                               json={"email": os.environ.get("GEOENGINE_EMAIL"),
                                     "password": os.environ.get("GEOENGINE_PASSWORD")}).json()
        elif token is not None:
            session = req.get(f'{server_url}/session', headers={'Authorization': f'Bearer {token}'}).json()
        elif "GEOENGINE_TOKEN" in os.environ:
            session = req.get(f'{server_url}/session',
                              headers={'Authorization': f'Bearer {os.environ.get("GEOENGINE_TOKEN")}'}).json()
        else:
            session = req.post(f'{server_url}/anonymous').json()

        if 'error' in session:
            raise GeoEngineException(session)

        self.__id = session['id']

        if 'validUntil' in session:
            self.__valid_until = session['validUntil']

        self.__server_url = server_url

    def __repr__(self) -> str:
        '''Display representation of a session'''
        r = ''
        r += f'Server:              {self.server_url}\n'
        r += f'Session Id:          {self.__id}\n'

        if self.__valid_until is not None:
            r += f'Session valid until: {self.__valid_until}\n'

        return r

    @property
    def auth_header(self) -> Dict[str, str]:
        '''
        Create an authentication header for the current session
        '''

        return {'Authorization': 'Bearer ' + self.__id}

    @property
    def server_url(self) -> str:
        '''
        Return the server url of the current session
        '''

        return self.__server_url

    def requests_bearer_auth(self) -> BearerAuth:
        '''
        Return a Bearer authentication object for the current session
        '''

        return BearerAuth(self.__id)

    def logout(self):
        '''
        Logout the current session
        '''

        req.post(f'{self.server_url}/logout', headers=self.auth_header)


def get_session() -> Session:
    '''
    Return the global session if it exists

    Raises an exception otherwise.
    '''

    if Session.session is None:
        raise UninitializedException()

    return Session.session


def initialize(server_url: str, credentials: Tuple[str, str] = None, token: str = None) -> None:
    '''
    Initialize communication between this library and a Geo Engine instance

    If credentials or a token are provided, the session will be authenticated.
    Credentials and token must not be provided at the same time.

    optional arugments: (email, password) as tuple or token as a string
    optional environment variables: GEOENGINE_EMAIL, GEOENGINE_PASSWORD, GEOENGINE_TOKEN
    optional .env file defining: GEOENGINE_EMAIL, GEOENGINE_PASSWORD, GEOENGINE_TOKEN
    '''

    load_dotenv()

    Session.session = Session(server_url, credentials, token)


def reset(logout: bool = True) -> None:
    '''
    Resets the current session
    '''

    if Session.session is not None and logout:
        Session.session.logout()

    Session.session = None
