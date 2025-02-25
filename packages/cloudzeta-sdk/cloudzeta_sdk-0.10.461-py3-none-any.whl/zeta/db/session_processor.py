from pathlib import Path
import os

from zeta.db.session import ZetaSession, ZetaSessionState
from zeta.utils.downloader import AssetDownloader
from zeta.utils.logging import zetaLogger
from zeta.utils.clip import compute_image_embeddings
from zeta.converter.base import ConvertData, BaseConverter
from zeta.converter.fbx import FbxConverter
from zeta.converter.gltf import GltfConverter
from zeta.converter.obj import ObjConverter
from zeta.converter.usdz import UsdzConverter
from zeta.sdk.asset import AssetUtils

class ZetaSessionProcessor(ZetaSession):
    def convert(self):
        self._init_resolver_context()

        zetaLogger.info(f"Converting for session {self._uid}, tmp path {self._workspace}")

        session_state = self.data.state
        if (session_state != ZetaSessionState.PROCESSING):
            raise ValueError(f"session is not in processing state, state={session_state}")

        root_asset_filename = AssetDownloader.download_asset(self.root_asset_blobname,
                                                             self._workspace)

        converter: BaseConverter = None

        if AssetUtils.is_unpacked_usd_asset(self.data.rootAssetPath):
            zetaLogger.info(f"Already in USD format, no need to convert: {self.data.rootAssetPath}")
            return
        elif AssetUtils.is_fbx_asset(self.data.rootAssetPath):
            converter = FbxConverter(self._workspace, root_asset_filename, self._resolver_context)
        elif AssetUtils.is_gltf_asset(self.data.rootAssetPath):
            converter = GltfConverter(self._workspace, root_asset_filename, self._resolver_context)
        elif AssetUtils.is_obj_asset(self.data.rootAssetPath):
            converter = ObjConverter(self._workspace, root_asset_filename, self._resolver_context)
        elif AssetUtils.is_usdz_asset(self.data.rootAssetPath):
            converter = UsdzConverter(self._workspace, root_asset_filename, self._resolver_context)
        else:
            zetaLogger.warning(f"Unsupported file format: {self.data.rootAssetPath}")
            return

        assert converter is not None

        for attempt in range(self._max_asset_retry):
            try:
                data: ConvertData = converter.extract()
                break  # Success
            except FileNotFoundError as e:
                asset_filepath = Path(e.filename)
                tmp_filepath = Path(self._workspace)
                asset_blobname: str = asset_filepath.relative_to(tmp_filepath).as_posix()
                zetaLogger.warning(f"Retry #{attempt+1}, download missing asset {asset_blobname}")
                AssetDownloader.download_asset(asset_blobname, self._workspace)
        else:
            raise ValueError(f"Error: Failed to convert file {root_asset_filename}")

        # Find a new empty blob prefix to host all converted assets.
        is_usdz: bool = AssetUtils.is_usdz_asset(self.data.rootAssetPath)
        converted_base: str = (f"unpacked_{Path(self.data.rootAssetPath).stem}" if is_usdz else
                               f"converted_{Path(self.data.rootAssetPath).stem}")
        converted_name: str = converted_base
        converted_blob_prefix: str = os.path.normpath(os.path.join(
            os.path.dirname(self.root_asset_blobname),
            converted_name,
        ))

        attempt: int = 0
        while True:
            attempt += 1
            if not self._blob_prefix_exists(converted_blob_prefix):
                break

            converted_name = f"{converted_base}_{attempt}"
            converted_blob_prefix = os.path.normpath(os.path.join(
                os.path.dirname(self.root_asset_blobname),
                converted_name,
            ))

        for asset_name, asset_filename in data.assets.items():
            asset_blobname: str = os.path.normpath(os.path.join(
                converted_blob_prefix,
                asset_name,
            ))

            if AssetUtils.is_asset_file_valid(asset_filename):
                zetaLogger.info(f"Uploading asset: {asset_filename} -> {asset_blobname}")
                self._bucket.upload_blob(asset_filename, asset_blobname)
            else:
                zetaLogger.error(f"Invalid asset file: {asset_filename}")

        new_root_asset_path: str = os.path.join(
            os.path.dirname(self.data.rootAssetPath),
            converted_name,
            os.path.basename(data.root_layer),
        )

        asset_prefix = self._get_asset_prefix(new_root_asset_path, self.data.rootAssetPath)

        thumbnail_blobname: str = None
        if AssetUtils.is_asset_file_valid(data.thumbnail_path):
            thumbnail_blobname = os.path.join(
                self._get_session_storage_path(self._uid),
                "__thumbnails",
                os.path.basename(data.thumbnail_path))
            self._bucket.upload_blob(data.thumbnail_path, thumbnail_blobname)

        thumbnail_embeddings = compute_image_embeddings(data.thumbnail_path)

        session_update = {
            "rootAssetPath": new_root_asset_path,
            "assetPrefix": asset_prefix,
            "thumbnailAsset": thumbnail_blobname,
            "thumbnailEmbeddings": thumbnail_embeddings,
        }

        # Create USDZ asset for all formats (expect for USDZ obviously)
        if data.usdz_asset is not None:
            new_usdz_asset_path: str = os.path.join(
                os.path.dirname(self.data.rootAssetPath),
                converted_name,
                os.path.basename(data.usdz_asset),
            )
            session_update["usdzAssetPath"] = new_usdz_asset_path

        self.update(session_update)
