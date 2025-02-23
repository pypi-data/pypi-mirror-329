from requests import Session

from .authenticator import AuthenticatorFactory, HttpClientFactory, AuthenticatorInterface
from .credentials import CredentialsInterface
from .parser import Parser


class ClientAbstract:
    USER_AGENT = "SDKgen Client v2.0"

    authenticator: AuthenticatorInterface = None
    http_client: Session = None
    parser: Parser = None

    def __init__(self, base_url: str, credentials: CredentialsInterface, version: str = None):
        self.authenticator = AuthenticatorFactory.factory(credentials)
        self.http_client = HttpClientFactory(self.authenticator, version).factory()
        self.parser = Parser(base_url)


class TagAbstract:
    http_client: Session = None
    parser: Parser = None

    def __init__(self, http_client: Session, parser: Parser):
        self.http_client = http_client
        self.parser = parser
