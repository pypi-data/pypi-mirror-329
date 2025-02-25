from google.cloud import storage
import datetime
import difflib
import os
import re

from zeta.storage.base import StorageBucket, BlobListResponse, BlobOp, BlobStat
from zeta.storage.utils import StorageConfig, StorageVendor
from zeta.utils.logging import zetaLogger


class GoogleStorageBucket(StorageBucket):
    def __init__(self, backend: StorageConfig):
        super().__init__(backend)

        assert self._config is not None
        assert self._config.vendor == StorageVendor.GCP, "Only GCP is supported"

        bucket_name_match = re.match(r"gs://([^/]+)$", self._config.url)
        assert bucket_name_match is not None, "Invalid bucket URL"

        self._bucket_name = bucket_name_match.group(1)
        secret_file: str = f"/secrets/storage/gcp/{self._bucket_name}.json"

        if os.path.exists(secret_file):
            self._client = storage.Client.from_service_account_json(secret_file)
        else:
            raise ValueError(f"Failed to find GCP credentials from: {secret_file}")

        self._bucket = self._client.bucket(self._bucket_name)

    def list_blobs(self, blob_prefix) -> BlobListResponse:
        """Lists all files in the bucket."""
        blob_names = []
        prefixes = []

        blobs = self._bucket.list_blobs(prefix=blob_prefix, delimiter="/")
        for blob in blobs:
            if not blob.name.endswith("/__zeta"):
                blob_names.append(blob.name)
        for prefix in blobs.prefixes:
            prefix = prefix.rstrip("/")
            prefixes.append(prefix)

        return BlobListResponse(blob_names=blob_names, prefixes=prefixes)

    def blob_stat(self, blob_name: str) -> BlobStat:
        blob = self._bucket.blob(blob_name)
        if not blob.exists():
            return None

        return BlobStat(name=blob.name, size=blob.size)

    def search_blob(self, blob_prefix: str, blob_basename: str) -> str:
        blobs = self._bucket.list_blobs(prefix=blob_prefix)
        target_blobs = {}

        for blob in blobs:
            blob_basename = os.path.basename(blob.name)
            target_blobs[blob_basename] = blob.name

        if len(target_blobs) == 0:
            zetaLogger.warning(f"no blobs found in prefix '{blob_prefix}'")
            return None

        closest_matches = difflib.get_close_matches(blob_basename, target_blobs.keys(), n=3, cutoff=0.0)
        return target_blobs.get(closest_matches[0]) if len(closest_matches) > 0 else None

    def download_blob(self, blob_name: str, destination_file_name: str):
        blob = self._bucket.blob(blob_name)
        blob.download_to_filename(destination_file_name)

    def upload_blob(self, file_path: str, destination_blob_name: str):
        blob = self._bucket.blob(destination_blob_name)
        content_disposition: str = f"attachment; filename={os.path.basename(file_path)}"
        blob.content_disposition = content_disposition
        blob.upload_from_filename(file_path)

    def sign_blob_operation(self, blob_name: str, operation: BlobOp, expiry: int) -> str:
        blob = self._bucket.blob(blob_name)

        if operation == BlobOp.GET and not blob.exists():
            zetaLogger.error(f"Failed to sign for GET, blob '{blob_name}' does not exist.")
            return None
        elif operation == BlobOp.PUT and blob.exists():
            zetaLogger.error(f"Failed to sign for PUT, blob '{blob_name}' already exists.")
            return None

        return blob.generate_signed_url(
            version="v4",
            method=operation.value,
            expiration=datetime.timedelta(seconds=expiry),
        )