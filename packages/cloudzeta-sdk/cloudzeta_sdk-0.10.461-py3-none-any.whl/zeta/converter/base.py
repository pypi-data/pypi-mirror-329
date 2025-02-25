from abc import ABC, abstractmethod
from pathlib import Path
from typing import List
import os
import subprocess

from pxr import Gf, Usd, UsdGeom, UsdUtils

from zeta.sdk.asset import AssetUtils
from zeta.sdk.uid import generate_uid
from zeta.usd.resolve import ResolverContext
from zeta.utils.logging import zetaLogger


# Must be synced with `OpenParameters` from usdzconvert/usdzconvert.
# We cannot directly use that class because it usdconvert is not exposed as a python package.
class UsdzConverterParameters(object):
    def __init__(self) -> None:
        self.copyTextures: bool = False
        self.searchPaths: List[str] = None
        self.verbose: bool = False
        self.metersPerUnit: int = 0 # set by converters


class ConvertData(object):
    def __init__(self) -> None:
        self.root_layer = None
        self.usdz_asset = None
        self.assets = {}
        self.thumbnail_path = None

class BaseConverter(ABC):
    def __init__(self, tmp_path: str, filename: str, context: ResolverContext) -> None:

        self._tmp_path: str = tmp_path
        self._filename: str = filename
        self._context: ResolverContext = context
        self._stage = None

    @abstractmethod
    def get_stage_path(self, asset_path) -> str:
        pass

    def extract(self) -> ConvertData:
        asset_basename: str = Path(self._filename).stem
        is_usdz: bool = AssetUtils.is_usdz_asset(self._filename)
        data = ConvertData()

        # Prepare a clean directory to convert the source file
        converted_name: str = asset_basename
        converted_path: str = os.path.join(self._tmp_path, converted_name)
        assert not os.path.exists(converted_path), f"unpack dir {converted_path} already exists"
        os.makedirs(converted_path)

        # Adobe's logic only supports assetsPath to be at the same level as the input file.
        stage_path = self.get_stage_path(converted_path)

        try:
            self._stage = Usd.Stage.Open(stage_path, self._context)
        except Exception as e:
            zetaLogger.error(f"Failed to open asset file: {e}")

        if not self._stage:
            raise ValueError("failed to open asset file")

        # Calculate bounding box
        self._calculate_bounding_box()

        # Backfill Up Axis
        self._backfill_up_axis()

        # Extract root layer
        root_layer = self._stage.GetRootLayer()
        root_layer_name: str = f"{converted_name}.usdc"
        root_layer_filename: str = os.path.join(converted_path, root_layer_name)
        usdz_name: str = f"exported_{asset_basename}.usdz"
        usdz_filename: str = os.path.join(converted_path, usdz_name)
        root_layer.Export(root_layer_filename)

        # Register root layer for upload
        data.root_layer = root_layer_name
        data.assets[root_layer_name] = root_layer_filename

        sublayer_paths, reference_paths, payload_paths = UsdUtils.ExtractExternalReferences(root_layer.identifier)
        if len(sublayer_paths) > 0 or len(payload_paths) > 0:
            raise ValueError("Unsupported external references in asset file, ",
                             "len(sublayer_paths)=", len(sublayer_paths),
                             ", len(payload_paths)=", len(payload_paths))

        for asset_path in reference_paths:
            asset_name = os.path.normpath(asset_path)
            asset_filename = os.path.join(converted_path, asset_name)
            if AssetUtils.is_asset_file_valid(asset_filename):
                data.assets[asset_name] = asset_filename
            else:
                zetaLogger.error(f"Invalid asset file: {asset_filename} when converting {root_layer.identifier}")

        # Create usdz package
        try:
            success = UsdUtils.CreateNewARKitUsdzPackage(root_layer_filename, usdz_filename)
            if not success:
                zetaLogger.error("Failed to create usdz file")
        except Exception as e:
            zetaLogger.error(f"Unexpected error when creating usdz file: {e}")

        if AssetUtils.is_asset_file_valid(usdz_filename):
            data.assets[usdz_name] = usdz_filename
            data.usdz_asset = usdz_name

        # Capture thumbnail
        thumbnail_path = os.path.join(self._tmp_path, f"{generate_uid()}.jpeg")
        if not self._capture_thumbnail(usdz_filename, thumbnail_path):
            zetaLogger.error("Failed to capture thumbnail")

        if AssetUtils.is_asset_file_valid(thumbnail_path):
            data.thumbnail_path = thumbnail_path

        return data

    def _calculate_bounding_box(self):
        if self._stage is None:
            raise RuntimeError("Stage not initialized")

        root_prim = self._stage.GetPseudoRoot()
        if not root_prim:
            raise RuntimeError("Root prim not found.")

        # Compute the bounding box
        bbox_cache = UsdGeom.BBoxCache(Usd.TimeCode.Default(), [UsdGeom.Tokens.default_])
        bbox = bbox_cache.ComputeWorldBound(root_prim)

        extent = bbox.ComputeAlignedRange()
        min_point = Gf.Vec3f(extent.GetMin())
        max_point = Gf.Vec3f(extent.GetMax())
        model_size = (max_point - min_point).GetLength()

        if model_size < 1:
            UsdGeom.SetStageMetersPerUnit(self._stage, 1.0)
        elif model_size < 10:
            UsdGeom.SetStageMetersPerUnit(self._stage, 0.1)

    def _backfill_up_axis(self):
        # Set the up axis if it is not set
        if not self._stage.HasAuthoredMetadata(UsdGeom.Tokens.upAxis):
            UsdGeom.SetStageUpAxis(self._stage, UsdGeom.Tokens.y)

    def _capture_thumbnail(self, input_path: str, output_path: str) -> None:
        command = ["zetaUsdCap", input_path, "--out", output_path, "--asyncTextureLoading", "1", "--geometryLoadBudget", "134217728"]
        zetaLogger.info(f"Executing zetaUsdCap: {' '.join(command)}")
        try:
            result = subprocess.run(command, check=True, timeout=300,
                                    stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            zetaLogger.info(f"Successfully executed zetaUsdCap:\n{result.stdout.decode()}")
            return True
        except subprocess.TimeoutExpired as e:
            zetaLogger.error(f"Timeout executing zetaUsdCap:\n{e.stdout.decode()}\n\n{e.stderr.decode()}")
            return False
        except subprocess.CalledProcessError as e:
            zetaLogger.error(f"Error executing zetaUsdCap (exit code {e.returncode}):\n{e.stdout.decode()}\n\n{e.stderr.decode()}")
            return False
