from datetime import datetime


def format_observation_datetime(datetime_obj: datetime) -> str:
    """
    Format datetime object to ISO 8601 format. Used for `observation_datetime` field in `Geometry`.
    """
    return datetime_obj.strftime('%Y-%m-%dT%H:%M:%S')
