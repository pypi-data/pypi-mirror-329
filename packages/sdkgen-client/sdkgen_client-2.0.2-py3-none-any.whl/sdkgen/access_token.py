import time
from typing import Optional

from pydantic import BaseModel, Field


class AccessToken(BaseModel):
    access_token: Optional[str] = Field(default=None, alias="access_token")
    token_type: Optional[str] = Field(default=None, alias="token_type")
    expires_in: Optional[int] = Field(default=None, alias="expires_in")
    refresh_token: Optional[str] = Field(default=None, alias="refresh_token")
    scope: Optional[str] = Field(default=None, alias="scope")

    def get_expires_in_timestamp(self):
        now = time.time()

        expires_in = self.expires_in
        if self.expires_in < 529196400:
            expires_in = now + expires_in

        return expires_in
