from datetime import timedelta

def format_time_delta(time_delta: timedelta) -> str:
    """
    Перетворює timedelta у формат MM:SS.mmm.
    :param time_delta: Різниця часу у вигляді timedelta.
    :return: Час у форматі MM:SS.mmm.
    """
    total_seconds = int(time_delta.total_seconds())
    milliseconds = int((time_delta.total_seconds() - total_seconds) * 1000)
    minutes, seconds = divmod(total_seconds, 60)
    return f"{minutes:01}:{seconds:02}.{milliseconds:03}"
