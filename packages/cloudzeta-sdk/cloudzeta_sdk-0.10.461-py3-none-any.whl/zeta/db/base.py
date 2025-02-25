from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass, fields
from datetime import datetime, timezone
from enum import Enum

from zeta.utils.logging import zetaLogger


@dataclass
class BaseData:
    """
    The unique identifier for this object.
    """
    uid: str

    """
    The name of this object. May be an empty string
    """
    name: str

    """
    The time this object was created, in ISO8601 format
    """
    createdAt: str

    """
    The time this object was updated, in ISO8601 format
    """
    updatedAt: str

    """
    The time this object was deleted, in ISO8601 format

    May be None if the object has not been deleted.
    """
    deletedAt: str


class ZetaBaseBackend(Enum):
    FIREBASE = "firebase"
    SUPABASE = "supabase"

class DefaultKeyDict(dict):
    def __missing__(self, key):
        # Optionally, you can set the key in the dictionary
        self[key] = key
        return key


lookup_data_class_field = DefaultKeyDict({
    "annotation_layer_uid": "annotationLayerUid",
    "annotation_uid": "annotationUid",
    "asset_prefix": "assetPrefix",
    "camera_metadata": "cameraMetadata",
    "created_at": "createdAt",
    "deleted_at": "deletedAt",
    "display_name": "displayName",
    "edit_layer_uid": "editLayerUid",
    "encrypted_token": "encryptedToken",
    "expires_at": "expiresAt",
    "external_asset_path": "externalAssetPath",
    "image_asset_path": "imageAsset",
    "is_ephemeral": "isEphemeral",
    "is_public": "isPublic",
    "is_published": "isPublished",
    "lora_path": "loraPath",
    "photo_url": "photoURL",
    "prim_path": "primPath",
    "project_uid": "projectUid",
    "root_asset_path": "rootAssetPath",
    "session_uid": "sessionUid",
    "storage_path": "storagePath",
    "storage_url": "storage.url",
    "storage_vendor": "storage.vendor",
    "thumbnail_asset_path": "thumbnailAsset",
    "thumbnail_embeddings": "thumbnailEmbeddings",
    "trigger_word": "triggerWord",
    "updated_at": "updatedAt",
    "usdz_asset_path": "usdzAssetPath",
    "user_uid": "userUid",
})

lookup_supabase_table_name = {
    "authTokens": "auth_tokens",
    "comments": "comments",
    "contactRequests": "contact_requests",
    "enhancements": "enhancements",
    "generations": "generations",
    "layers": "layers",
    "projects": "projects",
    "sessions": "sessions",
    "users": "users",
    "sceneSnapshots" : "scene_snapshots",
}

lookup_supabase_field_name = DefaultKeyDict({
    "annotationLayerUid": "annotation_layer_uid",
    "annotationUid": "annotation_uid",
    "assetPrefix": "asset_prefix",
    "cameraMetadata": "camera_metadata",
    "createdAt": "created_at",
    "deletedAt": "deleted_at",
    "displayName": "display_name",
    "editLayerUid": "edit_layer_uid",
    "encryptedToken": "encrypted_token",
    "expiresAt": "expires_at",
    "externalAssetPath": "external_asset_path",
    "imageAsset" : "image_asset_path",
    "isEphemeral": "is_ephemeral",
    "isPublic": "is_public",
    "isPublished": "is_published",
    "loraPath": "lora_path",
    "photoURL": "photo_url",
    "primPath": "prim_path",
    "projectUid": "project_uid",
    "rootAssetPath": "root_asset_path",
    "sessionUid": "session_uid",
    "storagePath": "storage_path",
    "thumbnailAsset": "thumbnail_asset_path",
    "thumbnailEmbeddings": "thumbnail_embeddings",
    "triggerWord": "trigger_word",
    "updatedAt": "updated_at",
    "usdzAssetPath": "usdz_asset_path",
    "userUid": "user_uid",
})


class ZetaBaseInterface(ABC):
    def __init__(self):
        self._parent: ZetaBaseInterface = None
        self._uid: str = None
        self._data = None

    @classmethod
    def create(cls, data):
        thiz = cls()
        thiz._create(data)
        return thiz

    def update(self, data):
        if "uid" in data and data["uid"] != self._uid:
            raise ValueError("UID mismatch")

        data["updatedAt"] = self._get_current_time()
        filtered_data = self._filter_data(data)

        if len(filtered_data) != len(data):
            # find the keys that were in data but not in the filtered data
            missing_keys = set(data.keys()) - set(filtered_data.keys())
            zetaLogger.warning(f"Unexpected key(s): {missing_keys}")

        self._update(filtered_data)

    @property
    def uid(self) -> str:
        return self._uid

    @property
    def data(self):
        return self._data

    def _data_from_dict(self, data: dict):
        if data is not None:
            self._data = self.data_class(**self._filter_data(data))

    def _filter_data(self, data: dict):
        field_names = {field.name for field in fields(self.data_class)}
        filtered_data = {}
        for key, value in data.items():
            firebase_key = lookup_data_class_field[key]
            if firebase_key in field_names:
                filtered_data[firebase_key] = value
            elif "." in firebase_key:
                nested_keys = firebase_key.split(".")
                nested_data = filtered_data
                for nested_key in nested_keys[:-1]:
                    if nested_key not in nested_data:
                        nested_data[nested_key] = {}
                    nested_data = nested_data[nested_key]
                nested_data[nested_keys[-1]] = value

        return filtered_data

    @staticmethod
    def _get_current_time() -> str:
        now = datetime.now(timezone.utc)
        return now.strftime("%Y-%m-%dT%H:%M:%SZ")

    """
    Implement the following methods in the derived classes
    """
    @classmethod
    @abstractmethod
    def get_schema_version(cls) -> int:
        pass

    @property
    @abstractmethod
    def table(self):
        pass

    @property
    @abstractmethod
    def backend(self) -> ZetaBaseBackend:
        pass

    @property
    @abstractmethod
    def collection_name(self) -> str:
        pass

    @property
    def table_name(self) -> str:
        return lookup_supabase_table_name[self.collection_name]

    @property
    @abstractmethod
    def data_class(self):
        pass

    @classmethod
    @abstractmethod
    def authenticate(cls, api_key: str, auth_token: str, refresh_token: str):
        pass

    @classmethod
    @abstractmethod
    def get_by_uid(cls, uid: str) -> ZetaBaseInterface:
        pass

    @classmethod
    @abstractmethod
    def get_by_name(cls, name: str) -> ZetaBaseInterface:
        pass

    @classmethod
    @abstractmethod
    def list_with_pagination(cls, page_size, page_token=None) -> list[ZetaBaseInterface]:
        pass

    @property
    @abstractmethod
    def valid(self) -> bool:
        pass

    @abstractmethod
    def _create(self, data) -> bool:
        pass

    @abstractmethod
    def _update(self, data):
        pass


class ZetaNestedInterface(ZetaBaseInterface):
    @property
    @abstractmethod
    def parent_uid_field(cls) -> str:
        pass

    @classmethod
    @abstractmethod
    def get_from_parent_collection(cls, parent: ZetaBaseInterface, uid: str):
        pass

    @classmethod
    @abstractmethod
    def get_by_name_from_parent_collection(cls, parent: ZetaBaseInterface, name: str):
        pass

    @classmethod
    @abstractmethod
    def create_in_parent_collection(cls, parent: ZetaBaseInterface, data):
        pass