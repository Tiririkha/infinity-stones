import uuid


def is_valid_uuid(uuid_to_check):
    """" Check if a string is a valid UUID """
    try:
        uuid.UUID(uuid_to_check)
        return True
    except ValueError:
        return False