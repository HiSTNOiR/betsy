def sanitise_for_logging(text):
    """Convert text to ASCII-safe format for logging, replacing non-ASCII characters with escape sequences."""
    if not isinstance(text, str):
        return str(text)

    try:
        # Try to encode and decode with utf-8, which preserves most characters
        return text
    except UnicodeError:
        # Fallback to ASCII with backslashreplace if needed
        return text.encode('ascii', 'backslashreplace').decode('ascii')
