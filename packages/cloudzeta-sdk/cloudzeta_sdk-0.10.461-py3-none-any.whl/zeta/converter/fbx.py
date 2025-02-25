from zeta.converter.base import BaseConverter


class FbxConverter(BaseConverter):
    def get_stage_path(self, asset_path) -> str:
        return f"{self._filename}:SDF_FORMAT_ARGS:fbxAssetsPath={asset_path}"


# if __name__ == "__main__":
#     from zeta.sdk.uid import generate_uid
#     from zeta.usd.resolve import AssetFetcher, ResolverContext

#     def download_asset(asset_blobname: str, temp_path: str):
#         return asset_blobname

#     fetcher = AssetFetcher.GetInstance()
#     fetcher.SetOnFetchCallback(download_asset)

#     tmp_path = f"/tmp/{generate_uid()}"
#     resolver_context = ResolverContext("/code/zeta/.firebase/assets/Textures", tmp_path)
#     converter = FbxConverter(tmp_path, "/code/zeta/.firebase/assets/BistroInterior.fbx", resolver_context)
#     update = converter.extract()
#     print(update.root_layer)
#     print(update.assets)