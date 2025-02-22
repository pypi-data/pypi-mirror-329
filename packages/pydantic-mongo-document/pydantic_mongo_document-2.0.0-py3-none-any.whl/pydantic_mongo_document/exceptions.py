class DocumentNotFound(Exception):
    def __init__(self, message: str | None = None) -> None:
        super().__init__(message or "Specified document doesn't exist.")
