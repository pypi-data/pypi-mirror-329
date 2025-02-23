from typing import Optional

from .access_token import AccessToken


class TokenStoreInterface:
    def get(self) -> AccessToken:
        pass

    def persist(self, token: AccessToken):
        pass

    def remove(self):
        pass


class MemoryTokenStore(TokenStoreInterface):
    token: Optional[AccessToken] = None

    def __init__(self):
        self.token = None

    def get(self) -> AccessToken:
        return self.token

    def persist(self, token: AccessToken):
        self.token = token

    def remove(self):
        self.token = None
