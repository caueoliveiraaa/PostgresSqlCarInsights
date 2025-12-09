"""Constants for mapping 'psycopg2' errors."""

from beartype.typing import Dict

ERROR_MAP: Dict[str, str] = {
    "42P04": "DuplicateDatabase - Database already exists.",
    "42P07": "DuplicateTable - Table already exists.",
    "42710": "DuplicateObject - Object already exists (index, schema, etc.).",
    "42701": "DuplicateColumn - Column already exists.",
    "23505": "UniqueViolation - Unique constraint violated.",
    "23503": "ForeignKeyViolation - Foreign key constraint violated.",
    "23514": "CheckViolation - Check constraint violated.",
    "23502": "NotNullViolation - NOT NULL constraint violated.",
    "42P01": "UndefinedTable - Table does not exist.",
    "42703": "UndefinedColumn - Column does not exist.",
    "42883": "UndefinedFunction - Function does not exist.",
    "3D000": "InvalidCatalogName - Database does not exist.",
    "42501": "InsufficientPrivilege - Permission denied.",
    "22001": "StringDataRightTruncation - Value too long for column.",
    "22003": "NumericValueOutOfRange - Number out of range.",
    "22007": "InvalidDatetimeFormat - Bad datetime format.",
    "40001": "SerializationFailure - Concurrent transaction conflict.",
    "40P01": "DeadlockDetected - Deadlock detected.",
}
