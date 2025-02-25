from __future__ import annotations
import os
import requests
import supabase
import time

# Force Python SDK to use Supabase by setting a dummy value
#TODO(CZ-768): Remove Firebase switch from db/__init__.py
os.environ["SUPABASE_URL"] = "dummy"

from zeta.db.supabase import ZetaSupabase
from zeta.sdk.asset import ZetaAsset
from zeta.utils.downloader import AssetDownloader
from zeta.utils.logging import zetaLogger
from zeta.utils.supabase import get_supabase_user_uid


CLOUD_ZETA_URL_PREFIX = "https://zetabase.ai"


class ZetaEngine(object):
    def __init__(self, zeta_url_prefix=CLOUD_ZETA_URL_PREFIX):
        self._zeta_url_prefix = zeta_url_prefix

        self._auth_token = None
        self._auth_token_expiry = 0
        self._token_uid: str = None
        self._encryption_key: str = None
        self._refresh_token = None
        self._user_uid = None

        config_response = requests.get(f"{self._zeta_url_prefix}/api/configs")
        if not config_response.ok:
            raise ValueError("Failed to get configs")
        config = config_response.json()

        SUPABASE_URL = config.get("SUPABASE_URL")
        SUPABASE_ANON_KEY = config.get("SUPABASE_ANON_KEY")

        if not SUPABASE_URL or not SUPABASE_ANON_KEY:
            raise ValueError("SUPABASE_URL and SUPABASE_ANON_KEY are not set")

        os.environ["SUPABASE_URL"] = SUPABASE_URL
        os.environ["SUPABASE_ANON_KEY"] = SUPABASE_ANON_KEY

        options = supabase.ClientOptions(auto_refresh_token=False)
        self._supabase_client = supabase.create_client(SUPABASE_URL, SUPABASE_ANON_KEY, options)

    def make_url(self, *elements) -> str:
        # Note that here os.path.join may not work as certain elements may start with a /
        return self._zeta_url_prefix + "/" + os.path.normpath("/".join(elements))

    def login(self, token_uid: str, encryption_key: str) -> bool:
        """
        Login with the given token_uid and encryption_key.

        @param token_uid: The token_uid to login with.
        @param encryption_key: The encryption_key to decrypt the token with.
        """
        if not token_uid or not encryption_key:
            zetaLogger.error("Token ID and/or encryption key is empty.")
            return False

        self._token_uid = token_uid
        self._encryption_key = encryption_key


        zeta_login_url = f"{self._zeta_url_prefix}/api/auth/token/login"
        response = requests.post(
            zeta_login_url,
            headers={
                "Content-Type": "application/json",
            },
            json={
                "authToken": token_uid,
                "encryptionKey": encryption_key,
            }
        )
        if not response.ok:
            zetaLogger.error(f"Failed to get auth token: {response.status_code} {response.text}")
            return False

        res = response.json()
        self._refresh_token = res.get("refreshToken")

        return self.refresh_auth_token()

    def refresh_auth_token(self) -> bool:
        """
        Refresh the authentication token from the refresh token.

        Must be called after login().
        """
        if not self._refresh_token:
            zetaLogger.error("Refresh token is empty.")
            return False

        if self._supabase_client:
            try:
                return self._refresh_supabase_auth_token()
            except Exception as e:
                zetaLogger.error(f"Failed to refresh supabase auth token {self._token_uid}: {e}")
                return False
        else:
            zetaLogger.error("Supabase client is not initialized")
            return False

    def _refresh_supabase_auth_token(self) -> bool:
        response = self._supabase_client.auth.refresh_session(self._refresh_token)

        if not response.session:
            zetaLogger.error(f"Failed to login with auth token: {response.error}")
            return False

        self._auth_token = response.session.access_token
        self._auth_token_expiry = int(time.time() + response.session.expires_in)

        response = self._supabase_client.auth.get_user(response.session.access_token)
        self._user_uid = get_supabase_user_uid(response.user)

        # Initialize the ZetaBase and AssetDownloader to use the supabase client.
        ZetaSupabase._db = self._supabase_client
        AssetDownloader.set_engine(self)

        return True

    def ensure_auth_token(method):
        def wrapper(self, *args, **kwargs):
            if not self._auth_token or self._auth_token_expiry < time.time():
                if not self.refresh_auth_token():
                    raise PermissionError("Failed to refresh auth token")

            return method(self, *args, **kwargs)
        return wrapper

    @ensure_auth_token
    def api_get(self, url: str, params: dict) -> requests.Response:
        if not self._auth_token:
            raise ValueError("Must login() before get()")
        if not url.startswith("/"):
            raise ValueError("URL must start with /")

        full_url: str = f"{self._zeta_url_prefix}{url}"
        return requests.get(
            full_url,
            headers={
                "Authorization": f"Bearer {self._auth_token}",
            },
            params=params
        )

    def _api_post(self, url: str, json: dict) -> requests.Response:
        if not self._auth_token:
            raise ValueError("Must login() before get()")
        if not url.startswith("/"):
            raise ValueError("URL must start with /")

        full_url: str = f"{self._zeta_url_prefix}{url}"
        return requests.post(
            full_url,
            headers={
                "Authorization": f"Bearer {self._auth_token}",
                "Content-Type": "application/json",
            },
            json=json
        )

    @ensure_auth_token
    def api_post(self, url: str, json: dict) -> requests.Response:
        return self._api_post(url, json)

    @ensure_auth_token
    def asset(self, owner_name: str, project_name: str, asset_path: str) -> ZetaAsset:
        return ZetaAsset(self, owner_name, project_name, asset_path)