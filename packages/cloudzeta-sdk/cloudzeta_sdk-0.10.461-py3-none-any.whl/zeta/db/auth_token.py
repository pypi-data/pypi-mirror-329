from datetime import datetime, timedelta, timezone
from dataclasses import dataclass

from zeta.db import BaseData, NestedZetaBase
from zeta.db.user import ZetaUser


@dataclass
class ZetaAuthTokenData(BaseData):
    """
    The encrypted token for this auth token.
    """
    encryptedToken: str

    """
    The time this token expires, in ISO8601 format
    """
    expiresAt: str

    """
    The user uid for this auth token.
    """
    userUid: str


class ZetaAuthToken(NestedZetaBase):
    @property
    def collection_name(self) -> str:
        return "authTokens"

    @property
    def parent_uid_field(cls) -> str:
        return "user_uid"

    @property
    def data_class(self):
        return ZetaAuthTokenData

    @staticmethod
    def get_expiration_time() -> str:
        now = datetime.now(timezone.utc)
        return (now + timedelta(days=60)).strftime("%Y-%m-%dT%H:%M:%SZ")

    def _create(self, data) -> bool:
        # Override the default _create method to add an expiration time
        data.update({
            "expiresAt": self.get_expiration_time(),
        })
        super()._create(data)


# Note: the following code is for testing purposes only. The keys should be invalidated.
if __name__ == "__main__":
    user = ZetaUser.get_by_uid("7B0QFQHq87gmHXfRj9L4vYWLBRi1")
    print(user.uid, user.valid, user.data)

    at1 = ZetaAuthToken.get_by_uid(user, "ly4xbih0e0kix2ew")
    print("at1", at1.uid, at1.data)

    at2 = ZetaAuthToken.get_by_uid("ly4xbih0e0kix2ew")
    print("at2", at2.uid, at2.data)

    new_auth_token = ZetaAuthToken.create_in_parent_collection(user, {
        "name": "python test",
        "encryptedToken": "test",
    })
    print(new_auth_token.uid, new_auth_token.data)