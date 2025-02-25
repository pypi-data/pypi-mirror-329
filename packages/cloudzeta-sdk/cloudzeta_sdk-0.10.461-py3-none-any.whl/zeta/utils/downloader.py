import difflib
import os
import requests

from zeta.db.user import ZetaUser
from zeta.sdk.asset import AssetPathComponents, AssetUtils
from zeta.storage.base import StorageBucket
from zeta.usd.resolve import AssetFetcher
from zeta.utils.logging import zetaLogger


class AssetDownloader(object):
    _engine = None
    _fetcher = AssetFetcher.GetInstance()

    @classmethod
    def has_engine(cls) -> bool:
        return cls._engine is not None

    @classmethod
    def set_engine(cls, engine):
        cls._engine = engine

    @classmethod
    def download_asset(cls, asset_blobname: str, temp_path: str):
        if cls._engine is not None:
            return cls._download_asset_via_zeta_engine(asset_blobname, temp_path)
        else:
            return cls._download_asset_via_google_storage(asset_blobname, temp_path)

    @classmethod
    def _download_asset_via_zeta_engine(cls, asset_blobname: str, temp_path: str):
        response = cls._engine.api_post("/api/asset/download", json={
            "blobName": asset_blobname
        })
        if not response.ok:
            error = response.json().get("error")
            zetaLogger.error(f"failed to download asset '{asset_blobname}': {error}")
            return ""

        signed_url = response.json().get("signedUrl")
        if not signed_url:
            zetaLogger.error(f"failed to get signed url for asset '{asset_blobname}'")
            return ""

        asset_filename: str = os.path.join(temp_path, asset_blobname)
        asset_dirname: str = os.path.dirname(asset_filename)
        if not os.path.exists(asset_dirname):
            os.makedirs(asset_dirname)

        try:
            with requests.get(signed_url, stream=True) as r:
                r.raise_for_status()
                with open(asset_filename, "wb") as f:
                    # Write the response content to the file in 64K chunks
                    for chunk in r.iter_content(chunk_size=65536):
                        f.write(chunk)
        except Exception as e:
            zetaLogger.error(f"failed to download asset '{asset_blobname}': {e}")
            return ""

        return asset_filename

    @classmethod
    def _search_blob_in_prefix(cls, bucket, asset_blobname: str):
        path_prefix = os.path.dirname(asset_blobname)
        asset_basename = os.path.basename(asset_blobname)

        blobs = bucket.list_blobs(prefix=path_prefix)
        target_blobs = {}

        for blob in blobs:
            blob_basename = os.path.basename(blob.name)
            target_blobs[blob_basename] = blob

        if len(target_blobs) == 0:
            zetaLogger.warning(f"no blobs found in prefix '{path_prefix}'")
            return None

        closest_matches = difflib.get_close_matches(asset_basename, target_blobs.keys(), n=3, cutoff=0.0)
        return target_blobs.get(closest_matches[0]) if len(closest_matches) > 0 else None

    @classmethod
    def _download_asset_via_google_storage(cls, asset_blobname: str, temp_path: str):
        asset_info: AssetPathComponents = AssetUtils.match_asset_path(asset_blobname)
        if not asset_info:
            zetaLogger.error(f"invalid asset blobname: {asset_blobname}")
            return ""

        owner: ZetaUser = ZetaUser.get_by_uid(asset_info.owner_uid)
        bucket: StorageBucket = StorageBucket.get_bucket_from_config(owner.storage)

        if not bucket.blob_stat(asset_blobname):
            blob_prefix = os.path.dirname(asset_blobname)
            blob_basename = os.path.basename(asset_blobname)
            fuzzy_blobname = bucket.search_blob(blob_prefix, blob_basename)
            if fuzzy_blobname is None:
                zetaLogger.warning(f"asset '{asset_blobname}' does not exist")
                return ""

            assert fuzzy_blobname.startswith(blob_prefix)
            zetaLogger.info(f"fuzzy match found for '{asset_blobname}': {fuzzy_blobname}")
            asset_blobname = fuzzy_blobname

        asset_filename: str = os.path.join(temp_path, asset_blobname)
        asset_dirname: str = os.path.dirname(asset_filename)
        if not os.path.exists(asset_dirname):
            os.makedirs(asset_dirname)
        bucket.download_blob(asset_blobname, asset_filename)

        return asset_filename


# Register the asset downloader callback. Note that we have to let the AssetDownloader class down
# the PyObject (i.e. AssetFetcher), so that destructor can be called in a proper order.
AssetDownloader._fetcher.SetOnFetchCallback(AssetDownloader.download_asset)