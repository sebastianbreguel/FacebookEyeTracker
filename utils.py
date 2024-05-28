from datetime import datetime, timezone, timedelta
def get_current_time_iso8601():
    # Get the current time in UTC
    now = datetime.now(timezone.utc)
    print(now)
    print(datetime.now())
    # Format the time in ISO 8601 with milliseconds
    formatted_time = now.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
    return formatted_time


def try_float(value):
    try:
        return float(value)
    except ValueError:
        return float("nan")


def linear_interpolate(start, end, steps):
    return [(start + (end - start) * i / steps) for i in range(1, steps)]






def subtract_seconds_from_datetime(datetime_str, seconds_to_subtract):
    """
    Subtract a specified number of seconds from a datetime string.

    Parameters:
    - datetime_str (str): The original datetime string in the format "YYYY-MM-DDTHH:MM:SS.sssZ".
    - seconds_to_subtract (int): The number of seconds to subtract from the datetime.

    Returns:
    - str: The new datetime string after subtracting the seconds, in the same format.
    """
    # Parse the datetime string into a datetime object
    datetime_obj = datetime.strptime(datetime_str, "%Y-%m-%dT%H:%M:%S.%fZ")

    # Subtract the specified number of seconds
    new_datetime_obj = datetime_obj - timedelta(seconds=seconds_to_subtract)

    # Convert the datetime object back into the desired string format
    new_datetime_str = new_datetime_obj.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"

    return new_datetime_str