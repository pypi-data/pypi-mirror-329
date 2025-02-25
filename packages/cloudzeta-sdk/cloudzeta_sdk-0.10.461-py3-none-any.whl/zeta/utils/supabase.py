import base64
import re
import uuid



class UidConverter:
    @staticmethod
    def is_valid_uuid(uuid_str: str) -> bool:
        """Check if string is a valid UUID"""
        uuid_pattern = re.compile(r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$", re.I)
        return bool(uuid_pattern.match(uuid_str))

    @staticmethod
    def is_valid_user_uid(uid: str) -> bool:
        """
        Validates if a string is a valid Firebase UID.
        User UIDs are either 28 characters (migrated from Firebase) or 22 characters (newly generated).

        Args:
            uid: Firebase-style UID to validate
        Returns:
            bool: True if valid Firebase UID format, False otherwise
        """
        if not isinstance(uid, str):
            return False

        # Firebase UIDs are 28 characters
        if len(uid) != 28 and len(uid) != 22:
            return False

        # Check if it only contains valid base64url characters
        return bool(re.match(r'^[A-Za-z0-9_-]+$', uid))

    @staticmethod
    def user_uid_to_uuid(uid: str) -> str:
        """
        Converts a Firebase-style UID back to a UUID.
        This is the inverse operation of uuid_to_user_uid.

        Args:
            uid: Firebase-style UID (28 characters)
        Returns:
            Standard UUID (e.g., "123e4567-e89b-12d3-a456-426614174000")
        """
        # Validate Firebase UID format
        if not UidConverter.is_valid_user_uid(uid):
            raise ValueError("Invalid Firebase UID format")

        # Take first 22 chars of Firebase UID
        base62_str = uid[:22]

        # Base62 characters (0-9, A-Z, a-z)
        BASE62_CHARS = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"

        # Convert from base62 to decimal
        decimal = 0
        for char in base62_str:
            decimal = decimal * 62 + BASE62_CHARS.index(char)

        # Convert decimal to hex, padding to 32 chars
        hex_str = format(decimal, 'x').zfill(32)

        # Format as UUID with hyphens
        uuid_str = f"{hex_str[:8]}-{hex_str[8:12]}-{hex_str[12:16]}-{hex_str[16:20]}-{hex_str[20:32]}"

        # Validate the resulting UUID
        try:
            uuid.UUID(uuid_str)
        except ValueError as e:
            raise ValueError(f"Resulting UUID is invalid: {e}")

        return uuid_str

    @staticmethod
    def uuid_to_user_uid(uuid: str) -> str:
        """
        Converts a UUID to a Firebase-style UID.
        This is a deterministic conversion - the same UUID will always produce the same Firebase UID.

        Args:
            uuid: Standard UUID (e.g., "123e4567-e89b-12d3-a456-426614174000")
        Returns:
            Firebase-style UID (28 characters)
        """
        # Validate UUID format
        if not UidConverter.is_valid_uuid(uuid):
            raise ValueError("Invalid UUID format")

        # Remove hyphens from UUID
        clean_uuid = uuid.replace("-", "")

        # Convert hex to decimal using big integers to handle large values
        decimal = int(clean_uuid, 16)

        # Base62 characters (0-9, A-Z, a-z)
        BASE62_CHARS = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"

        # Convert to base62
        base62 = ""
        remaining = decimal

        # Handle special case when decimal is 0
        if remaining == 0:
            base62 = "0"

        # Convert to base62 string by repeatedly dividing by 62
        while remaining > 0:
            remainder = remaining % 62
            base62 = BASE62_CHARS[remainder] + base62
            remaining = remaining // 62

        # Pad with zeros if needed to reach 22 chars
        padded_base62 = base62.zfill(22)
        return padded_base62


def get_supabase_user_uid(user) -> str:
    if user.user_metadata.get("fbuser"):
        return user.user_metadata.get("fbuser").get("uid")
    else:
        return UidConverter.uuid_to_user_uid(user.id)