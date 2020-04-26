import logging


def cut_text(text: str, limit: int, warning_text: str or None = None):
    if warning_text is None:
        warning_text = f'Limit is {limit} text will be cut'
    if len(text) > limit:
        logging.warning(warning_text)
        text = text[:limit - 3] + '...'
    return text


def is_url(path: str):
    return ('https://' in path) or ('http://' in path)


def auto_type(path: str) -> str:
    expansion = path.split('.')[-1].upper()
    if expansion in {'PNG', 'JPEG', 'JPG', 'GIF', 'TIFF', 'TIF', 'BMP', 'RAW', 'WEBP'}:
        return 'photo'

    if is_url(path):
        logging.warning(f'Auto type function detected url: {path}.\n'
                        f'Auto type will work incorrect if there is no file expansion at the end of url!')
    return 'document'

