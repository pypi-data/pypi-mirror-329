from dataclasses import dataclass

from zeta.db import BaseData, NestedZetaBase
from zeta.utils.logging import zetaLogger

try:
    # TODO(CZ-921): Add proper dependencies to Comfy worker.
    from zeta.db.session import ZetaSession
except ImportError:
    zetaLogger.warning("ImportError: ZetaSession not found")


@dataclass
class SceneSnapshotData(BaseData):
    # The user that took the snapshot.
    userUid: str

    # The session that this snapshot is associated with.
    sessionUid: str

    # The camera metadata that was used for this snapshot.
    cameraMetadata: dict

    # Image asset path
    imageAsset: str


class ZetaSceneSnapshot(NestedZetaBase):
    @classmethod
    def get_by_uid(cls, uid: str) -> 'ZetaSceneSnapshot':
        # This may not work in Firebase.
        thiz = super().get_by_uid(uid)
        thiz._parent = ZetaSession.get_by_uid(thiz.data.sessionUid)
        return thiz

    @property
    def collection_name(cls) -> str:
        return "sceneSnapshots"

    @property
    def parent_uid_field(cls) -> str:
        return "session_uid"

    @property
    def data_class(self):
        return SceneSnapshotData

    @property
    def session_uid(self) -> str:
        return self._parent.uid

    @classmethod
    def list_for_session(cls, session_uid: str) -> list['ZetaSceneSnapshot']:
        thiz = cls()
        query = thiz.table.select("*").eq("session_uid", session_uid).is_("deleted_at", None)
        try:
            data = query.execute().data
            snapshots = []
            for item in data:
                snapshot = ZetaSceneSnapshot()
                snapshot._data_from_dict(item)
                snapshots.append(snapshot)
            return snapshots
        except Exception as e:
            zetaLogger.error(f"Failed to query scene snapshots for session_uid='{session_uid}': {e}")
            return []
