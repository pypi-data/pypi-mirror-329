from zeta.converter.base import BaseConverter


class GltfConverter(BaseConverter):
    def get_stage_path(self, asset_path) -> str:
        return f"{self._filename}:SDF_FORMAT_ARGS:gltfAssetsPath={asset_path}"
