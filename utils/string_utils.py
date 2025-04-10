def sanitise_for_logging(text):
    """Convert text to ASCII-safe format for logging, replacing non-ASCII characters with escape sequences.

    Args:
        text: The string to sanitise

    Returns:
        ASCII-safe string suitable for logging systems with encoding limitations
    """
    if not isinstance(text, str):
        return str(text)
    return text.encode('ascii', 'backslashreplace').decode('ascii')
