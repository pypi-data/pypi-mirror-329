from zeta.converter.base import BaseConverter


class ObjConverter(BaseConverter):
    def get_stage_path(self, asset_path) -> str:
        return f"{self._filename}:SDF_FORMAT_ARGS:objAssetsPath={asset_path}&objPhong=true"


if __name__ == "__main__":
    from zeta.sdk.uid import generate_uid
    from zeta.usd.resolve import AssetFetcher, ResolverContext

    def download_asset(asset_blobname: str, temp_path: str):
        return asset_blobname

    fetcher = AssetFetcher.GetInstance()
    fetcher.SetOnFetchCallback(download_asset)

    tmp_path: str = f"/tmp/{generate_uid()}"
    resolver_context = ResolverContext("/code/zeta/.firebase/assets/dam/", tmp_path)
    converter = ObjConverter(tmp_path, "dam.obj", resolver_context)
    # resolver_context = ResolverContext("/code/zeta/.firebase/assets/slide/", tmp_path)
    # converter = ObjConverter(tmp_path, "slide.obj", resolver_context)
    update = converter.extract()
    print(update.root_layer)
    print(update.assets)