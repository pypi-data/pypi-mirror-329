from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import List

from zeta.storage.utils import StorageConfig, StorageVendor


@dataclass
class BlobListResponse(object):
    """ Files directly under a prefix. """
    blob_names: List[str]

    """ Other prefixes that nest directly under a prefix. """
    prefixes: List[str]

    def is_empty(self) -> bool:
        return len(self.blob_names) == 0 and len(self.prefixes) == 0


@dataclass
class BlobStat(object):
    """ Metadata for a blob. """
    name: str
    size: int


class BlobOp(Enum):
    GET = "GET"
    PUT = "PUT"


class StorageBucket(ABC):
    def __init__(self, config: StorageConfig):
        self._config = config

    @staticmethod
    def get_bucket_from_config(storage: StorageConfig) -> StorageConfig:
        from zeta.storage.azure import AzureStorageBucket
        from zeta.storage.gcp import GoogleStorageBucket

        if storage.vendor == StorageVendor.AWS:
            raise NotImplementedError("AWS storage is not implemented yet.")
        elif storage.vendor == StorageVendor.AZURE:
            return AzureStorageBucket(storage)
        elif storage.vendor == StorageVendor.GCP:
            return GoogleStorageBucket(storage)
        else:
            raise ValueError(f"Unsupported storage vendor: {storage.vendor}")

    @staticmethod
    def get_bucket(vendor: StorageVendor, url: str) -> StorageConfig:
        return StorageBucket.get_bucket_from_config(StorageConfig(vendor=vendor, url=url))

    @abstractmethod
    def list_blobs(self, blob_prefix) -> BlobListResponse:
        """Lists all blobs and prefix directly under the `blob_prefix`."""
        pass

    @abstractmethod
    def blob_stat(self, blob_name: str) -> BlobStat:
        """Returns metadata for a blob."""
        pass

    @abstractmethod
    def search_blob(self, blob_prefix: str, blob_basename: str) -> str:
        """Fuzzy search for a blob by basename under the `blob_prefix`.

        Returns the full blob name if found, otherwise returns None.
        """
        pass

    @abstractmethod
    def download_blob(self, blob_name: str, destination_file_path: str):
        """Downloads a file from the bucket."""
        pass

    @abstractmethod
    def upload_blob(self, file_path: str, destination_blob_name: str):
        """Uploads a file to the bucket."""
        pass

    @abstractmethod
    def sign_blob_operation(self, blob_name: str, operation: BlobOp, expiry: int) -> str:
        """Generate a signed URL for the specified blob operation.

        operation: The operation to be performed (GET or PUT).
                   For GET operations, the signed blob must exist.
                   For PUT operations, the signed blob must not exist.
        expiry: The expiration time for the signed URL in seconds.

        Returns a signed URL or None if the operation is not supported.
        """
        pass