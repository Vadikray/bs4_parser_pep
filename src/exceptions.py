class ParserFindTagException(Exception):
    """Вызывается, когда парсер не может найти тег."""

    pass


class ContentExclusion(Exception):
    """Вызывается, когда парсер не может найти контент."""

    pass
