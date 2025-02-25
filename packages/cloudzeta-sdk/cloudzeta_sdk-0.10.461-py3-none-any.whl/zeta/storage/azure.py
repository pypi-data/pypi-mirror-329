from azure.storage.blob import ContainerClient, ContentSettings, BlobClient, BlobProperties, BlobPrefix, generate_blob_sas, BlobSasPermissions
from datetime import datetime, timedelta, timezone
import difflib
import json
import os
import re

from zeta.storage.base import StorageBucket, BlobListResponse, BlobOp, BlobStat
from zeta.storage.utils import StorageConfig, StorageVendor
from zeta.utils.logging import zetaLogger


class AzureStorageBucket(StorageBucket):
    def __init__(self, backend: StorageConfig):
        super().__init__(backend)

        assert self._config is not None
        assert self._config.vendor == StorageVendor.AZURE, "Only Azure is supported"

        url_match = re.match(r"https://([^/]+).blob.core.windows.net/([^/]+)", self._config.url)
        assert url_match is not None, "Invalid container URL"

        self._account_name = url_match.group(1)
        self._container_name = url_match.group(2)

        secret_file = f"/secrets/storage/azure/{self._account_name}.json"
        with open(secret_file) as f:
            self._secret = json.load(f)

        self._container = ContainerClient(
            account_url=f"https://{self._account_name}.blob.core.windows.net/",
            container_name=self._container_name,
            credential=self._secret["key"],
        )

    def list_blobs(self, blob_prefix) -> BlobListResponse:
        blob_names = []
        prefixes = []

        blobs = self._container.walk_blobs(name_starts_with=blob_prefix, delimiter="/")
        for blob in blobs:
            if isinstance(blob, BlobProperties):
                if not blob.name.endswith("/__zeta"):
                    blob_names.append(blob.name)
            elif isinstance(blob, BlobPrefix):
                prefix = blob.name.rstrip("/")
                prefixes.append(prefix)

        return BlobListResponse(blob_names=blob_names, prefixes=prefixes)

    def blob_stat(self, blob_name: str) -> BlobStat:
        blob: BlobClient = self._container.get_blob_client(blob_name)
        if not blob.exists():
            return None

        properties = blob.get_blob_properties()
        return BlobStat(name=blob_name, size=properties.size)

    def search_blob(self, blob_prefix: str, blob_basename: str) -> str:
        blobs = self._container.list_blobs(name_starts_with=blob_prefix)
        target_blobs = {}

        for blob in blobs:
            blob_base_name = os.path.basename(blob.name)
            target_blobs[blob_base_name] = blob.name

        if not target_blobs:
            zetaLogger.warning(f"no blobs found in prefix '{blob_prefix}'")
            return None

        closest_matches = difflib.get_close_matches(blob_basename, target_blobs.keys(), n=3, cutoff=0.0)
        return target_blobs.get(closest_matches[0]) if closest_matches else None

    def download_blob(self, blob_name: str, destination_file_name: str):
        blob: BlobClient = self._container.get_blob_client(blob_name)
        with open(destination_file_name, "wb") as file:
            downloader = blob.download_blob()
            file.write(downloader.readall())

    def upload_blob(self, file_path: str, destination_blob_name: str):
        blob: BlobClient = self._container.get_blob_client(destination_blob_name)
        content_disposition = f"attachment; filename={os.path.basename(file_path)}"
        content_settings = ContentSettings(content_disposition=content_disposition)
        with open(file_path, "rb") as data:
            blob.upload_blob(data, overwrite=True, content_settings=content_settings)

    def sign_blob_operation(self, blob_name: str, operation: BlobOp, expiry: int) -> str:
        permissions: BlobSasPermissions = None
        if operation == BlobOp.GET:
            permissions = BlobSasPermissions(read=True)
        elif operation == BlobOp.PUT:
            permissions = BlobSasPermissions(write=True, create=True)
        else:
            raise ValueError(f"Invalid operation {operation.value}")

        saa_token = generate_blob_sas(
            account_name=self._account_name,
            account_key=self._secret["key"],
            container_name=self._container_name,
            blob_name=blob_name,
            permission=permissions,
            expiry=datetime.now(timezone.utc) + timedelta(seconds=expiry),
        )

        return f"https://{self._account_name}.blob.core.windows.net/{self._container_name}/{blob_name}?{saa_token}"