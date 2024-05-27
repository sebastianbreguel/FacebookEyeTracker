from datetime import datetime, timezone


def get_current_time_iso8601():
    # Get the current time in UTC
    now = datetime.now(timezone.utc)
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
