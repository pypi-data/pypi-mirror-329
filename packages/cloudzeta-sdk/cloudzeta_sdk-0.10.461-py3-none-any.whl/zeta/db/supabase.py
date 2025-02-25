from __future__ import annotations
from dataclasses import fields
from postgrest.exceptions import APIError
import supabase
import threading

from zeta.db.base import ZetaBaseBackend, ZetaBaseInterface, ZetaNestedInterface, lookup_supabase_field_name
from zeta.sdk.uid import generate_uid
from zeta.utils.logging import zetaLogger


class ZetaSupabase(ZetaBaseInterface):
    _db: supabase.Client = None
    _db_lock = threading.Lock()

    def __init__(self):
        super().__init__()

        self._uid = None
        self._table = None

    @classmethod
    def get_schema_version(cls) -> str:
        dummy = cls()
        response = dummy._db.table("schema_migrations") \
            .select("*") \
            .order("version", desc=True) \
            .limit(1) \
            .execute()

        return response.data[0]["version"] if response.data else None

    @property
    def backend(self) -> ZetaBaseBackend:
        return ZetaBaseBackend.SUPABASE

    @staticmethod
    def _ensure_db_connection():
        if not ZetaSupabase._db:
            raise ValueError("Supabase is not initialized")

    @property
    def table(self) -> supabase.Table:
        if not self._table:
            ZetaSupabase._ensure_db_connection()
            self._table = ZetaSupabase._db.table(self.table_name)

        return self._table

    @classmethod
    def authenticate(cls, api_key: str, auth_token: str, refresh_token: str):
        raise NotImplementedError("ZetaSupabase authentication: not implemented")

    @classmethod
    def get_by_uid(cls, uid: str) -> ZetaSupabase:
        thiz = cls()
        thiz._uid = uid

        try:
            data = thiz.table.select("*").eq("uid", uid).single().execute().data
            thiz._data_from_dict(data)
        except APIError as e:
            zetaLogger.error(f"Failed to query document for uid '{uid}': code={e.code}")

        return thiz

    @classmethod
    def get_by_name(cls, name: str) -> ZetaSupabase:
        thiz = cls()

        query_res = thiz.table.select("*").eq("name", name).execute().data
        if len(query_res) == 0:
            zetaLogger.error(f"document not found for name: {name}")
        elif len(query_res) > 1:
            zetaLogger.error(f"multiple documents found for name: {name}")
        else:
            thiz._uid = query_res[0]["uid"]
            thiz._data_from_dict(query_res[0])

        return thiz

    @classmethod
    def list_with_pagination(cls, page_size, page_token=None) -> list[ZetaSupabase]:
        dummy = cls()
        query = dummy.table.select("*").order("created_at", desc=True).limit(page_size)

        if page_token:
            # Retrieve the last record to get the cursor (created_at)
            last_record: ZetaSupabase = cls.get_by_uid(page_token)
            if last_record:
                last_created_at = last_record.data.createdAt
                query = query.lt("created_at", last_created_at)
            else:
                zetaLogger.error(f"Invalid page token: {page_token}")
                return []

        try:
            records = query.execute().data
            result = []

            for record in records:
                thiz = cls()
                thiz._uid = record["uid"]
                try:
                    thiz._data_from_dict(record)
                except Exception as e:
                    zetaLogger.error(f"Error creating object: {e}, uid={thiz._uid}")
                    continue
                result.append(thiz)

            return result

        except APIError as e:
            zetaLogger.error(f"Failed to query records with pagination: code='{e.code}'")
            return []

    @property
    def valid(self) -> bool:
        return self.table is not None and self._data is not None and self._uid is not None

    def _create(self, data) -> bool:
        # Prepare the default base data
        self._uid = generate_uid()

        created_at = self._get_current_time()
        base_data = {
            "uid": self._uid,
            "name": "",
            "created_at": created_at,
            "updated_at": created_at,
            "deleted_at": None,
        }

        # Merge base data with provided data
        extended_data = {}
        extended_data.update(base_data)
        for k, v in data.items():
            extended_data[lookup_supabase_field_name[k]] = v

        # If there is a parent, set the foreign key
        if self._parent:
            extended_data[self.parent_uid_field] = self._parent._uid

        # Check for required fields
        required_fields = {lookup_supabase_field_name[field.name] for field in fields(self.data_class)}
        missing_keys = required_fields - extended_data.keys()
        if missing_keys:
            raise ValueError(f"Missing required fields: {missing_keys}")

        try:
            # Insert the new record into Supabase
            self.table.insert(extended_data).execute()
            self._data_from_dict(extended_data)
            zetaLogger.info(f"Record created successfully with uid: {self._uid}")
            return True
        except APIError as e:
            # Handle specific API errors
            zetaLogger.error(f"Failed to create record for uid='{self._uid}' code={e.code}")
            return False

    def _update(self, data):
        if not self.valid:
            zetaLogger.error("Invalid record")
            return

        filtered_data = {}
        for k, v in data.items():
            filtered_data[lookup_supabase_field_name[k]] = v

        try:
            # Perform the update operation
            self.table.update(filtered_data).eq("uid", self._uid).execute()
            record = self.table.select("*").eq("uid", self._uid).single().execute().data
            self._data_from_dict(record)
        except APIError as e:
            # Handle specific API errors
            zetaLogger.error(f"Failed to update record for uid='{self._uid}' code={e.code}")
            return

    @classmethod
    def search_vector(
        cls,
        user_id: str,
        vector_field: str,
        embeddings: list[float],
        fields: str,
        limit: int = 10,
        filter_condition: str = '',
    ):
        thiz = cls()
        try:
            response = thiz._db.rpc(
                "vector_search",
                {
                    "user_id": user_id,
                    "table_name": thiz.table_name,
                    "vector_field": vector_field,
                    "query_vector": embeddings,
                    "limit_count": limit,
                    "fields": fields,
                    "filter_condition": filter_condition,
                }
            ).execute()

            # Unwrap 'result' from response.data
            cleaned_response = []
            if hasattr(response, 'data'):
                for item in response.data:
                    if isinstance(item, dict) and 'result' in item:
                        cleaned_response.append(item['result'])
            else:
                print("Response does not contain a 'data' attribute.")

            return cleaned_response
        except Exception as e:
            zetaLogger.error(f"Failed to perform vector search: {e}")
            return []


class NestedZetaSupabase(ZetaSupabase, ZetaNestedInterface):
    def __init__(self):
        super().__init__()

        self._parent: ZetaSupabase = None

    @classmethod
    def get_from_parent_collection(cls, parent: ZetaSupabase, uid: str):
        thiz = cls()
        thiz._uid = uid
        thiz._parent = parent

        query = thiz.table.select("*").eq("uid", uid).eq(thiz.parent_uid_field, parent.uid)
        try:
            data = query.single().execute().data
            thiz._data_from_dict(data)
        except APIError as e:
            zetaLogger.error(f"Failed to query document for uid='{uid}', {thiz.parent_uid_field}='{parent.uid}': code={e.code}")

        return thiz

    @classmethod
    def get_by_name_from_parent_collection(cls, parent: ZetaSupabase, name: str):
        thiz = cls()
        thiz._parent = parent

        query = thiz.table.select("*").eq("name", name).eq(thiz.parent_uid_field, parent.uid)
        try:
            data = query.single().execute().data
            thiz._uid = data["uid"]
            thiz._data_from_dict(data)
        except APIError as e:
            zetaLogger.error(f"Failed to query document for name='{name}', {thiz.parent_uid_field}='{parent.uid}': code={e.code}")

        return thiz

    @classmethod
    def create_in_parent_collection(cls, parent: ZetaSupabase, data):
        thiz = cls()
        thiz._parent = parent
        thiz._create(data)
        return thiz