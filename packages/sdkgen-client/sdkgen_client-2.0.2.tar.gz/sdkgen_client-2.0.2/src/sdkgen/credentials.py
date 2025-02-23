from typing import Optional

from .token_store import TokenStoreInterface


class CredentialsInterface:
    pass


class Anonymous(CredentialsInterface):
    pass


class ApiKey(CredentialsInterface):
    token: str = None
    name: str = None
    in_: str = None

    def __init__(self, token: str, name: str, in_: str):
        self.token = token
        self.name = name
        self.in_ = in_


class HttpBasic(CredentialsInterface):
    username: str = None
    password: str = None

    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password


class HttpBearer(CredentialsInterface):
    def __init__(self, token: str):
        self.token = token


class OAuth2(CredentialsInterface):
    client_id: str = None
    client_secret: str = None
    token_url: str = None
    authorization_url: str = None
    token_store: Optional[TokenStoreInterface] = None
    scopes: Optional[list[str]] = None

    def __init__(self, client_id: str, client_secret: str, token_url: str, authorization_url: str,
                 token_store: Optional[TokenStoreInterface], scopes: Optional[list[str]]):
        self.client_id = client_id
        self.client_secret = client_secret
        self.token_url = token_url
        self.authorization_url = authorization_url
        self.token_store = token_store
        self.scopes = scopes
