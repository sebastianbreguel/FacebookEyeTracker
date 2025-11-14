import winsound
from datetime import datetime, timedelta, timezone


def get_current_time_iso8601(option: int = 1) -> str:
    # Get the current time in UTC
    now = datetime.now(timezone.utc)
    # Format the time in ISO 8601 with milliseconds\
    if option == 1:
        formatted_time = now.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
    elif option == 2:
        # for the screenshots
        formatted_time = now.strftime("%Y-%m-%dT%H_%M_%S")

    return formatted_time


def try_float(value: str) -> float:
    try:
        return float(value)
    except ValueError:
        return float("nan")


def linear_interpolate(start: float, end: float, steps: int) -> list[float]:
    return [(start + (end - start) * i / steps) for i in range(1, steps)]


def make_beep() -> None:
    frequency = 1000  # Set Frequency To 2500 Hertz
    duration_beep = 1000  # Set Duration To 1000 ms == 1 second
    winsound.Beep(frequency, duration_beep)  # type: ignore
    return None


def subtract_seconds_from_datetime(datetime_str: str, seconds_to_subtract: int) -> str:
    """
    Subtract a specified number of seconds from a datetime string.

    Parameters
    ----------
    datetime_str : str
        The original datetime string in the format "YYYY-MM-DDTHH:MM:SS.sssZ".
    seconds_to_subtract : int
        The number of seconds to subtract from the datetime.

    Returns
    -------
    str
        The new datetime string after subtracting the seconds, in the same format.
    """
    # Parse the datetime string into a datetime object
    datetime_obj = datetime.strptime(datetime_str, "%Y-%m-%dT%H:%M:%S.%fZ")

    # Subtract the specified number of seconds
    new_datetime_obj = datetime_obj - timedelta(seconds=seconds_to_subtract)

    # Convert the datetime object back into the desired string format
    new_datetime_str = new_datetime_obj.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"

    return new_datetime_str
