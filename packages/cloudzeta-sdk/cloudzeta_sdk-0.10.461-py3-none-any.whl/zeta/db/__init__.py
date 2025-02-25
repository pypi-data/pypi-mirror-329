import os

from zeta.db.base import ZetaBaseBackend, BaseData
from zeta.utils.logging import zetaLogger

SUPABASE_URL = os.getenv("SUPABASE_URL")

if SUPABASE_URL:
    zetaLogger.info("Using Supabase backend")
    from zeta.db.supabase import ZetaSupabase as ZetaBase
    from zeta.db.supabase import NestedZetaSupabase as NestedZetaBase
else:
    zetaLogger.info("Using Firebase backend")
    from zeta.db.firebase import ZetaFirebase as ZetaBase
    from zeta.db.firebase import NestedZetaFirebase as NestedZetaBase