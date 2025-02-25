from __future__ import annotations
from cryptography.fernet import Fernet
from firebase_admin import auth as firebase_admin_auth
from flask import request, jsonify
from functools import wraps
from urllib.parse import urlparse, parse_qs
import firebase_admin
import os
import requests
import supabase
import time

from zeta.utils.logging import zetaLogger
from zeta.utils.supabase import UidConverter, get_supabase_user_uid


SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY")

# GOOGLE_APPLICATION_CREDENTIALS is only used for local development for Firebase authentication.
# For production (using Google Cloud Run), the auth is handled by the Google Cloud Run service.
# For Supabase authentication, we use the environment variables SUPABASE_URL and
# SUPABASE_SERVICE_KEY.
GOOGLE_APPLICATION_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

def create_firebase_auth():
    def verify_auth(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            auth_header = request.headers.get("Authorization")
            if auth_header:
                token = auth_header.split(" ")[1]
            else:
                return jsonify({"error": "Missing token"}), 403

            try:
                decoded_token = firebase_admin_auth.verify_id_token(token)
                request.user_id = decoded_token["user_id"]
            except Exception as e:
                return jsonify({"error": str(e)}), 403

            return f(*args, **kwargs)

        return decorated_function
    return verify_auth


def create_supabase_auth(supabase_url, supabase_service_key):
    client: supabase.Client = supabase.create_client(supabase_url, supabase_service_key)
    user_cache: dict[str, dict[supabase.UserResponse, int]] = {}

    def verify_auth(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            auth_header = request.headers.get("Authorization")
            if not auth_header:
                return jsonify({"error": "Missing token"}), 403

            try:
                token = auth_header.split(" ")[1]

                response: supabase.UserResponse = None
                if token in user_cache:
                    cached_response, expiry = user_cache[token]
                    if expiry > time.time():
                        response = cached_response

                if not response:
                    response = client.auth.get_user(token)
                    user_cache[token] = (response, time.time() + 300)

                if not response or not response.user:
                    return jsonify({"error": "Invalid token"}), 403

                user_id = get_supabase_user_uid(response.user)

                # Add user info to request
                request.user_id = user_id
            except ValueError as e:
                return jsonify({"error": str(e)}), 403
            except Exception as e:
                return jsonify({"error": f"Authentication failed: {str(e)}"}), 403

            return f(*args, **kwargs)
        return decorated_function
    return verify_auth


verify_auth = None

if SUPABASE_URL and SUPABASE_SERVICE_KEY:
    verify_auth = create_supabase_auth(SUPABASE_URL, SUPABASE_SERVICE_KEY)
else:
    # Use the default credentials, which will pull credentials from
    # GOOGLE_APPLICATION_CREDENTIALS automatically.
    # https://cloud.google.com/docs/authentication/application-default-credentials
    cred = firebase_admin.credentials.ApplicationDefault()
    firebase_admin.initialize_app(cred)
    verify_auth = create_firebase_auth()

def encrypt_token(token: str, encryption_key: bytes = None) -> tuple[str, str]:
    if encryption_key is None:
        encryption_key = Fernet.generate_key()

    fernet = Fernet(encryption_key)
    return fernet.encrypt(token.encode()).decode(), encryption_key.decode()

def decrypt_token(encrypted_token: str, encryption_key: bytes) -> str:
    fernet = Fernet(encryption_key)
    return fernet.decrypt(encrypted_token.encode()).decode()


def generate_new_auth_token(user_uid: str, refresh_token: str):
    if SUPABASE_URL and SUPABASE_SERVICE_KEY:
        return _generate_new_supabase_auth_token(user_uid)
    else:
        # TODO: Grab a new refresh token from Firebase authentication service instead of reuse the
        # refreshToken.
        return encrypt_token(refresh_token)


def _generate_new_supabase_auth_token(user_uid: str) -> str:
    encryption_key = Fernet.generate_key()

    fernet = Fernet(encryption_key)
    return fernet.encrypt(user_uid.encode()).decode(), encryption_key.decode()


def create_new_supabase_user_session(user_uid: str) -> str:
    supabase_uuid: str = UidConverter.user_uid_to_uuid(user_uid)

    zetaLogger.info(f"Creating new session for user {supabase_uuid}")
    client: supabase.Client = supabase.create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)

    user_response = client.auth.admin.get_user_by_id(supabase_uuid)
    if not user_response or not user_response.user:
        raise ValueError(f"Failed to get user {supabase_uuid}: {user_response.error}")

    link_response = client.auth.admin.generate_link({
        "type": "magiclink",
        "email": user_response.user.email
    })

    hashed_token = link_response.properties.hashed_token
    action_link = f"{SUPABASE_URL}/auth/v1/verify?token={hashed_token}&type=magiclink"
    signed_response = requests.get(action_link, allow_redirects=False)
    if signed_response.status_code != 303:
        raise ValueError(f"Failed to create magic link: HTTP {signed_response.status_code}")

    magic_link = signed_response.headers.get("Location")
    if not magic_link:
        raise ValueError("Failed to get magic link")

    parsed_url = urlparse(magic_link)
    parsed_params = parse_qs(parsed_url.fragment)
    refresh_tokens = parsed_params.get("refresh_token")
    if not refresh_tokens or type(refresh_tokens) != list or len(refresh_tokens) != 1:
        raise ValueError(f"Failed to parse refresh token")

    return refresh_tokens[0]