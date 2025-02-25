from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
import re

from zeta.db import BaseData, ZetaBase
from zeta.storage.utils import StorageConfig, StorageVendor


class ZetaUserTier(Enum):
    ANONYMOUS = -1
    FREE = 0
    PRO = 1
    ENTERPRISE = 2
    ADMIN = 42

class ZetaUserRole(Enum):
    NONE = None
    OWNER = "owner"
    EDITOR = "editor"
    VIEWER = "viewer"

class ZetaAddons(Enum):
    NONE = None
    GENERATOR = "generator"

@dataclass
class ZetaUserData(BaseData):
    displayName: str
    email: str
    photoURL: str
    tier: ZetaUserTier
    addons: list[str] = field(default_factory=list)
    # TODO: remove default value once all users are backfilled.
    storage: StorageConfig = None


class ZetaUser(ZetaBase):
    @property
    def collection_name(cls) -> str:
        return "users"

    @property
    def data_class(self):
        return ZetaUserData

    @property
    def is_paying(self) -> bool:
        return self._data.tier in [ZetaUserTier.PRO, ZetaUserTier.ENTERPRISE, ZetaUserTier.ADMIN]

    @property
    def storage(self) -> StorageConfig:
        storage_data = self._data.storage
        storage = None

        if storage_data and storage_data.get("vendor") and storage_data.get("url"):
            storage = StorageConfig(**self._data.storage)
            storage.vendor = StorageVendor(storage.vendor)
        else:
            storage = StorageConfig.create_default()
        return storage

    def get_gcp_bucket_name(self) -> str:
        # TODO: Support other storage vendors
        assert self.storage is not None
        assert self.storage.vendor == StorageVendor.GCP, "Only GCP is supported"

        bucket_name_match = re.match(r"gs://([^/]+)$", self.storage.url)
        assert bucket_name_match is not None, "Invalid bucket URL"

        return bucket_name_match.group(1)

    def _data_from_dict(self, data: dict) -> ZetaUserData:
        super()._data_from_dict(data)
        if self._data and type(self._data.tier) == int:
            self._data.tier = ZetaUserTier(self._data.tier)

    # Disable creating a new user
    #   Unlike ZetaBase, uid must be provided for ZetaUser (i.e. we cannot create a new user).
    #   In reality, the ZetaUser class must be created after user sign up and the UID comes
    #   from the authentication service.
    def _create(self, data) -> bool:
        raise NotImplementedError