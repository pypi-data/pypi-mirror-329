from zeta.db import BaseData, NestedZetaBase, ZetaBaseBackend
from dataclasses import dataclass


@dataclass
class ZetaProjectData(BaseData):
    storagePath: str

    isPublic: bool
    isPublished: bool
    roles: dict[str, str]

@dataclass
class ZetaProjectDataSupabase(ZetaProjectData):
    userUid: str

class ZetaProject(NestedZetaBase):
    @property
    def collection_name(self) -> str:
        return "projects"

    @property
    def parent_uid_field(cls) -> str:
        return "user_uid"

    @property
    def data_class(self):
        if self.backend == ZetaBaseBackend.FIREBASE:
            return ZetaProjectData
        elif self.backend == ZetaBaseBackend.SUPABASE:
            return ZetaProjectDataSupabase
        else:
            raise ValueError(f"Invalid backend: {self.backend}")

    @property
    def user_uid(self) -> str:
        if self._parent is not None:
            return self._parent.uid
        elif self._data.userUid is not None:
            return self._data.userUid
        else:
            raise ValueError("User UID not found")

    def get_session_storage_path(self, session_uid: str) -> str:
        if not self.data.storagePath.endswith("/main"):
            raise ValueError(f"Invalid project storage path: {self.data.storagePath}")

        # Replace "/main" with f"/{session_id}"
        return self.data.storagePath[:-5] + f"/{session_uid}"