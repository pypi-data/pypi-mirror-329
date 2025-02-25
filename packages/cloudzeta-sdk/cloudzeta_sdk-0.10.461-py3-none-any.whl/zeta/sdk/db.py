import os

# Force Python SDK to use Supabase by setting a dummy value
#TODO(CZ-768): Remove Firebase switch from db/__init__.py
os.environ["SUPABASE_URL"] = "dummy"

from zeta.db.session import ZetaSession, ZetaSessionData


__all__ = [
    "ZetaSession",
    "ZetaSessionData",
]