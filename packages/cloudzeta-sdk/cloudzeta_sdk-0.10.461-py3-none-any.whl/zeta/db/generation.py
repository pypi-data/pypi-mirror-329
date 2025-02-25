from dataclasses import dataclass
from enum import Enum

from zeta.db import BaseData, NestedZetaBase
from zeta.utils.logging import zetaLogger


try:
    # TODO(CZ-921): Add proper dependencies to Comfy worker.
    from zeta.db.session import ZetaSession
except ImportError:
    zetaLogger.warning("ImportError: ZetaSession not found")


"""
The type of generation that was performed.

Must match the enum in the `GenerationType` class in the `engine/db/generation.ts` file.
"""
class GenerationType(Enum):
    TEXT_TO_IMAGE = "TEXT_TO_IMAGE"
    TEXT_TO_3D = "TEXT_TO_3D"
    IMAGE_TO_3D = "IMAGE_TO_3D"
    SCENE_TO_IMAGE = "SCENE_TO_IMAGE"
    SCENE_TO_VIDEO = "SCENE_TO_VIDEO"


"""
The state of the generation.

Must match the enum in the `GenerationState` class in the `engine/db/generation.ts` file.
"""
class GenerationState(Enum):
    IDLE = "Idle"

    PENDING = "Pending"
    GENERATING = "Generating"

    DONE = "Done"
    ERROR = "Error"
    CANCELLED = "Cancelled"

"""
The backend that was used to generate the generation.

Must match the enum in the `GenerationBackend` class in the `engine/db/generation.ts` file.
"""
class GenerationBackend(Enum):
    COMFYUI = "COMFYUI"
    MESHY_V4_PREVIEW = "MESHY_V4_PREVIEW"
    TRIPO = "TRIPO"


@dataclass
class GenerationData(BaseData):
    # The type of generation that was performed.
    type: GenerationType

    # The backend that was used to generate the generation.
    backend: GenerationBackend

    # The state of the generation.
    state: GenerationState

    # The progress of the generation.
    progress: int

    # The error message that was generated if the generation failed.
    error: str

    # The user that requested the generation.
    userUid: str

    # The session that this generation is associated with.
    sessionUid: str

    # The prim path of the object that was generated.
    primPath: str

    # The prompt that was used for this generation.
    prompt: dict

    # The camera metadata that was used for this generation.
    cameraMetadata: dict

    # The outputs (e.g. images, videos, etc.) that were generated.
    outputs: list[dict]


class ZetaGeneration(NestedZetaBase):
    @classmethod
    def get_by_uid(cls, uid: str) -> 'ZetaGeneration':
        # This may not work in Firebase.
        thiz = super().get_by_uid(uid)
        thiz._parent = ZetaSession.get_by_uid(thiz.data.sessionUid)
        return thiz

    @property
    def collection_name(cls) -> str:
        return "generations"

    @property
    def parent_uid_field(cls) -> str:
        return "session_uid"

    @property
    def data_class(self):
        return GenerationData

    @property
    def session_uid(self) -> str:
        return self._parent.uid
    
    def get_scene_snapshot_uids(self) -> list['str']:
        if self.data is None:
            zetaLogger.error("Generation data is empty")
            return []
        try:
            snapshot_uids = self.data.cameraMetadata.get('snapshotUids', [])
            return snapshot_uids
        except Exception as e:
            zetaLogger.error(f"Failed to get camera snapshots: {e}")

        return []
