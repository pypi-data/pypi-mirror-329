from __future__ import annotations
from dataclasses import fields
from typing import Callable, List

from google.api_core.exceptions import PermissionDenied
from google.cloud import firestore
from google.cloud.firestore_v1 import DocumentSnapshot
from google.oauth2 import credentials

from zeta.db.base import ZetaBaseBackend, BaseData, ZetaBaseInterface, ZetaNestedInterface
from zeta.sdk.uid import generate_uid
from zeta.utils.logging import zetaLogger


CLOUD_ZETA_PROJECT_ID = "gozeta-prod"
GOOGLE_AUTH_URL = "https://securetoken.googleapis.com/v1/token"


# Base class for all database classes
# The Typescript version of this file is located: src/engine/db/base.ts
class ZetaFirebase(ZetaBaseInterface):
    _db: firestore.Client = None

    def __init__(self):
        super().__init__()

        if not ZetaFirebase._db:
            ZetaFirebase._db = firestore.Client()

        self._collection: firestore.CollectionReference = None
        self._ref: firestore.DocumentReference = None
        self._on_update: Callable[[BaseData], None] = None

    @classmethod
    def get_schema_version(cls) -> str:
        return None

    @property
    def table(self):
        raise NotImplementedError("table property is not applicable for ZetaFirebase")

    @property
    def backend(self) -> ZetaBaseBackend:
        return ZetaBaseBackend.FIREBASE

    @classmethod
    def authenticate(cls, api_key: str, auth_token: str, refresh_token: str):
        cred = credentials.Credentials(
            auth_token, refresh_token, client_id="", client_secret="",
            token_uri=f"{GOOGLE_AUTH_URL}?key={api_key}")
        cls._db = firestore.Client(CLOUD_ZETA_PROJECT_ID, cred)
        assert cls._db is not None

    @classmethod
    def get_by_uid(cls, uid: str) -> ZetaFirebase:
        thiz = cls()
        thiz._collection = cls._db.collection(thiz.collection_name)
        thiz._uid = uid
        thiz._ref = thiz._collection.document(thiz._uid)
        thiz._data_from_dict(thiz._ref.get().to_dict())
        return thiz

    @classmethod
    def get_by_name(cls, name: str) -> ZetaFirebase:
        thiz = cls()
        thiz._collection = thiz._db.collection(thiz.collection_name)

        query = thiz._collection.where(filter=firestore.FieldFilter("name", "==", name))
        query_res = query.get()

        if len(query_res) == 0:
            zetaLogger.error(f"document not found for name: {name}")
        elif len(query_res) > 1:
            zetaLogger.error(f"multiple documents found for name: {name}")
        else:
            thiz._uid = query_res[0].id
            thiz._ref = query_res[0].reference
            thiz._data_from_dict(query_res[0].to_dict())

        return thiz

    @classmethod
    def list_with_pagination(cls, page_size, page_token=None) -> list[ZetaFirebase]:
        dummy = cls()
        collection = cls._db.collection(dummy.collection_name)
        query = collection.order_by("createdAt", direction=firestore.Query.DESCENDING)

        if page_token:
            doc = collection.document(page_token).get()
            if doc.exists:
                query = query.start_after(doc)
            else:
                zetaLogger.error(f"Invalid page token: {page_token}")
                return []

        query = query.limit(page_size)
        docs = query.stream()

        result = []
        for doc in docs:
            thiz = cls()
            thiz._uid = doc.id
            thiz._ref = doc.reference
            try:
                thiz._data_from_dict(doc.to_dict())
            except Exception as e:
                zetaLogger.error(f"Error creating object: {e}, uid={thiz._uid}")
                continue
            result.append(thiz)
        return result

    @property
    def valid(self) -> bool:
        return self._ref is not None and self._ref.get().exists and self._data is not None

    def _create(self, data) -> bool:
        # Create a new document with a random uid
        self._uid = generate_uid()
        self._collection = (self._db.collection(self.collection_name) if self._parent is None else
                            self._parent._ref.collection(self.collection_name))
        self._ref = self._collection.document(self._uid)

        if self._ref.get().exists:
            zetaLogger.error("Document already exists")
            return False

        created_at = self._get_current_time()
        base_data = {
            "uid": self._uid,
            "name": "",
            "createdAt": created_at,
            "updatedAt": created_at,
            "deletedAt": None,
        }
        extended_data = {}
        extended_data.update(base_data)
        extended_data.update(data)

        # check if the data is missing any required fields
        if len(extended_data) != len(fields(self.data_class)):
            field_names = {field.name for field in fields(self.data_class)}
            missing_keys = set(field_names) - set(extended_data.keys())
            raise ValueError(f"Missing required fields: {missing_keys}")

        self._ref.set(base_data)
        self.update(extended_data)

        return True

    def _update(self, data):
        self._ref.update(data)
        self._data_from_dict(self._ref.get().to_dict())

    def _handle_snapshot(self, doc_snapshot: List[DocumentSnapshot], _1, _2):
        if len(doc_snapshot) != 1:
            raise ValueError("Unexpected number of documents in snapshot")

        doc = doc_snapshot[0]
        # TODO: handle changes
        self._data_from_dict(doc.to_dict())
        self._on_update(self._data)

    def on_update(self, callback: Callable[[BaseData], None]):
        if not self.valid:
            raise ValueError("on_update() called on invalid object")

        self._on_update = callback
        self._ref.on_snapshot(self._handle_snapshot)

    @classmethod
    def search_vector(
        cls,
        user_uid: str,
        vector_field: str,
        embeddings: list[float],
        fields: str,
        limit: int = 10,
        filter_condition: str = '',
    ):
        pass

class NestedZetaFirebase(ZetaFirebase, ZetaNestedInterface):
    def __init__(self):
        super().__init__()

        self._parent: ZetaFirebase = None

    @classmethod
    def get_by_uid(cls, uid: str) -> ZetaFirebase:
        thiz = cls()

        thiz._parent = None
        thiz._collection = thiz._db.collection_group(thiz.collection_name)

        query = thiz._collection.where(filter=firestore.FieldFilter("uid", "==", uid))

        try:
            query_res = query.get()
        except PermissionDenied:
            explain: str = "Permission denied while directly querying nested object by uid."
            raise ValueError(f"{thiz.collection_name}/{uid}: {explain}") from None

        if len(query_res) == 0:
            zetaLogger.error(f"document not found for uid: {uid}")
        elif len(query_res) > 1:
            zetaLogger.error(f"multiple documents found for uid: {uid}")
        else:
            thiz._uid = query_res[0].id
            thiz._ref = query_res[0].reference
            thiz._data_from_dict(query_res[0].to_dict())

        return thiz

    @classmethod
    def get_from_parent_collection(cls, parent: ZetaFirebase, uid: str):
        thiz = cls()
        thiz._parent = parent
        thiz._collection = thiz._parent._ref.collection(thiz.collection_name)
        thiz._uid = uid
        thiz._ref = thiz._collection.document(thiz._uid)
        thiz._data_from_dict(thiz._ref.get().to_dict())

        return thiz

    @classmethod
    def get_by_name_from_parent_collection(cls, parent: ZetaFirebase, name: str):
        thiz = cls()
        thiz._parent = parent
        thiz._collection = thiz._parent._ref.collection(thiz.collection_name)

        query = thiz._collection.where(filter=firestore.FieldFilter("name", "==", name))
        query_res = query.get()

        if len(query_res) == 0:
            zetaLogger.error(f"document not found for name: {name}")
        elif len(query_res) > 1:
            zetaLogger.error(f"multiple documents found for name: {name}")
        else:
            thiz._uid = query_res[0].id
            thiz._ref = query_res[0].reference
            thiz._data_from_dict(query_res[0].to_dict())

        return thiz

    @classmethod
    def create_in_parent_collection(cls, parent: ZetaFirebase, data):
        thiz = cls()
        thiz._parent = parent
        thiz._create(data)
        return thiz