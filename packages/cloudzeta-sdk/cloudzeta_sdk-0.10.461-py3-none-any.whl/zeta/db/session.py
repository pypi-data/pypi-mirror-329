from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from postgrest.exceptions import APIError
import os
import re
import shutil

from pxr import Sdf, Usd, Tf, UsdUtils

from zeta.db import BaseData, ZetaBase, ZetaBaseBackend
from zeta.db.layer import ZetaLayer
from zeta.db.project import ZetaProject
from zeta.db.user import ZetaUser
from zeta.sdk.asset import AssetUtils
from zeta.sdk.uid import generate_uid
from zeta.storage.base import BlobListResponse, StorageBucket
from zeta.usd.resolve import ResolverContext
from zeta.utils.downloader import AssetDownloader
from zeta.utils.logging import zetaLogger


class ZetaSessionState(Enum):
    """
    The state of the session
    """
    INIT = "init"
    PROCESSING = "processing"
    READY = "ready"
    ERROR = "error"


@dataclass
class ZetaSessionData(BaseData):
    projectUid: str
    rootAssetPath: str
    externalAssetPath: str
    assetPrefix: list[str]

    # If true, the session will be public and readable to all registered users.
    isPublic: bool

    # If true, the session will be published the the Internet and readable to all users who have
    # a link to the session.
    isPublished: bool

    # Ephemeral sessions do not need a registered user to create.
    #
    # If true, the session will be automatically deleted in a certain period of time after it
    # becomes inactive.
    isEphemeral: bool

    roles: dict[str, str]
    state: ZetaSessionState;

    annotationLayerUid: str;
    editLayerUid: str;

    error: str;
    thumbnailAsset: str;
    thumbnailEmbeddings: list[float];
    usdzAssetPath: str;


class ZetaSession(ZetaBase):
    _max_asset_retry: int = 1024

    def __init__(self):
        super().__init__()

        self._stage: Usd.Stage = None

        self._workspace: str = None
        self._owner: ZetaUser = None
        self._bucket: StorageBucket = None
        self._project: ZetaProject = None
        self._resolver_context: ResolverContext = None
        self._edit_layer: ZetaLayer = None

    @property
    def collection_name(cls) -> str:
        return "sessions"

    @property
    def data_class(self):
        return ZetaSessionData

    @property
    def stage(self) -> Usd.Stage:
        return self._stage

    @property
    def root_asset_blobname(self) -> str:
        assert self._project is not None, "Project not loaded"

        # Note that we can't use os.path.join here because root_asset_path is an absolute path.
        return os.path.normpath(f"{self._project.data.storagePath}/{self._data.rootAssetPath}")

    @property
    def owner_uid(self) -> str:
        owners = [uid for uid, role in self._data.roles.items() if role == "owner"]
        if len(owners) == 0:
            raise ValueError("Owner not found")
        if len(owners) > 1:
            raise ValueError("Multiple owners found")
        return owners[0]

    def _data_from_dict(self, data: dict):
        if self.backend == ZetaBaseBackend.FIREBASE:
            if "thumbnailEmbeddings" not in data:
                data["thumbnailEmbeddings"] = None

        super()._data_from_dict(data)

        if self._data and type(self._data.state) == str:
            self._data.state = ZetaSessionState(self._data.state)

    def _push_edit_layer_updates(self, *args):
        self._edit_layer.push_updates()

    def _update_state_firebase(self, from_state: str, to_state: str) -> bool:
        with self._db.transaction(max_attempts=1):
            session_data = self._ref.get()
            state: str = session_data.get("state")

            if (state != from_state):
                zetaLogger.error(f"invalid state transition: {self._uid}, state={state}")
                return False

            self.update({ "state": to_state })
            return True

    def _update_state_supabase(self, from_state: str, to_state: str) -> bool:
        try:
            self.table.update({
                "state": to_state,
                "updated_at": self._get_current_time(),
            }).eq("uid", self._uid).eq("state", from_state).execute()

            record = self.table.select("*").eq("uid", self._uid).single().execute().data
            self._data_from_dict(record)
        except APIError as e:
            zetaLogger.error(f"Failed to update state: {self._uid}, state={from_state}, code={e.code}")
            return False

        return True

    def update_state(self, from_state: ZetaSessionState, to_state: ZetaSessionState) -> bool:
        assert self.valid, "Invalid session object."

        if self.backend == ZetaBaseBackend.FIREBASE:
            return self._update_state_firebase(from_state.value, to_state.value)
        elif self.backend == ZetaBaseBackend.SUPABASE:
            return self._update_state_supabase(from_state.value, to_state.value)
        else:
            raise ValueError(f"Invalid backend: {self.backend}")

    def update_error(self, error: str) -> None:
        self.update({
            "error": error,
        })

    def _init_resolver_context(self):
        assert self._workspace is None, "Workspace already initialized"
        self._workspace = f"/tmp/{generate_uid()}"

        assert self._owner is None, "Owner already loaded"
        self._owner = ZetaUser.get_by_uid(self.owner_uid)

        if not AssetDownloader.has_engine():
            # When asset downloader deoes not come with ZetaEngine, We are running in the server
            # backend. We need to initialize the asset downloader with the engine.
            assert self._bucket is None, "Bucket already loaded"
            try:
                self._bucket = StorageBucket.get_bucket_from_config(self._owner.storage)
            except ValueError as e:
                zetaLogger.error(f"Failed to get bucket: {e}")

        assert self._project is None, "Project already loaded"
        self._project = ZetaProject.get_from_parent_collection(self._owner, self._data.projectUid)
        if not self._project.valid:
            zetaLogger.warning(f"Project not found in user collection, getting by uid: {self._data.projectUid}")
            self._project = ZetaProject.get_by_uid(self._data.projectUid)

        # Validate the project storage path
        project_match = re.match(r"^users/([^/]+)/projects/([^/]+)/([^/]+)$",
                                 self._project.data.storagePath)
        assert project_match, f"Invalid project storage path: {self._project.data.storagePath}"

        owner_uid, project_uid, _ = project_match.groups()
        assert owner_uid == self._project.user_uid, f"Invalid project storage path: {self._project.data.storagePath}, {owner_uid} != {self._project.user_uid}"
        assert project_uid == self._project.uid, f"Invalid project storage path: {self._project.data.storagePath}, {project_uid} != {self._project.uid}"

        assert self._resolver_context is None, "Session already loaded"
        root_dir: str = os.path.dirname(self.root_asset_blobname)
        self._resolver_context = ResolverContext(root_dir, self._workspace)

    def load_stage(self) -> Usd.Stage:
        """
        Load the session into an OpenUSD stage.

        @param workspace (optional): The workspace directory where the asssets will be downloaded.
                                     If None, a temporary directory will be automatically created.
        @return: The OpenUSD stage.
        """
        if self._stage is not None:
            zetaLogger.warning("Session already loaded")
            return self._stage

        self._init_resolver_context()
        self._edit_layer = ZetaLayer.get_from_parent_collection(self, self._data.editLayerUid)

        if self._edit_layer is None:
            raise ValueError("Edit layer is not found")

        self._edit_layer.load_layer()
        if self._edit_layer.layer is None:
            raise ValueError("Edit layer is not loaded")

        root_asset_filename: str = AssetDownloader.download_asset(self.root_asset_blobname,
                                                                  self._workspace)

        self._stage = Usd.Stage.Open(root_asset_filename, self._resolver_context)
        if self._stage is None:
            raise ValueError("Stage is not loaded")

        session_layer: Sdf.Layer = self._stage.GetSessionLayer()
        if session_layer is None:
            raise ValueError("Session layer is not found")

        session_layer.subLayerPaths.append(self._edit_layer.layer.identifier)
        self._stage.SetEditTarget(self._edit_layer.layer)

        self._listener = Tf.Notice.Register(
            Usd.Notice.StageContentsChanged,
            self._push_edit_layer_updates,
            self._stage)

        return self._stage

    def export_usdz(self, output_dir: str) -> str:
        """
        Export the session as a USDZ file.

        @param output_dir: The path to the output directory.

        @return: The path to the USDZ file.
        """
        if not os.path.exists(output_dir):
            raise ValueError(f"Output path does not exist: {output_dir}")
        if not os.path.isdir(output_dir):
            raise ValueError(f"Output path is not a directory: {output_dir}")
        if not self._stage:
            self.load_stage()

        working_dir: str = os.path.dirname(self._stage.GetRootLayer().identifier)
        zetaLogger.info(f"USDZ export working dir: {working_dir}")

        flattened_root_layer: Sdf.Layer = self._stage.Flatten()
        flattened_stage: Usd.Stage = Usd.Stage.Open(flattened_root_layer, self._resolver_context)

        flattened_stage.RemovePrim("/ZetaScene")
        usdc_root_asset_path = os.path.join(working_dir, f"{generate_uid()}.usdc")
        usdz_export_path = os.path.join(working_dir, f"{generate_uid()}.usdz")
        flattened_stage.Export(usdc_root_asset_path)

        zetaLogger.info(f"USDZ export usdc path: {usdc_root_asset_path}")
        zetaLogger.info(f"USDZ export usdz path: {usdz_export_path}")

        try:
            success = UsdUtils.CreateNewARKitUsdzPackage(usdc_root_asset_path, usdz_export_path)
            if not success:
                zetaLogger.error("Failed to create usdz file")
        except Exception as e:
            zetaLogger.error(f"Unexpected error when creating usdz file: {e}")

        usdz_output_path = os.path.join(output_dir, f"zeta-export-{generate_uid()}.usdz")
        # Move the usdz file to the output directory
        shutil.move(usdz_export_path, usdz_output_path)

        zetaLogger.info(f"USDZ export output path: {usdz_output_path}")
        return usdz_output_path

    def _blob_prefix_exists(self, blob_prefix: str) -> bool:
        blobs: BlobListResponse = self._bucket.list_blobs(blob_prefix)
        return not blobs.is_empty()

    def _get_asset_prefix(self, root_asset_path, external_asset_path) -> list:
        unique_prefixes = set()

        unique_prefixes.add(root_asset_path)
        unique_prefixes.update(AssetUtils.get_all_parent_paths(root_asset_path))

        if external_asset_path is not None:
            unique_prefixes.add(external_asset_path)
            unique_prefixes.update(AssetUtils.get_all_parent_paths(external_asset_path))

        return list(unique_prefixes)

    def _get_session_storage_path(self, session_uid: str) -> str:
        project_storage_path: str = self._project.data.storagePath

        if not project_storage_path.endswith("/main"):
            raise ValueError(f"Invalid project storage path: {project_storage_path}")

        # Replace "/main" with f"/{session_id}"
        return project_storage_path[:-5] + f"/{session_uid}"
