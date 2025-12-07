class LLMServiceError(Exception):
    def __init__(self, message: str, status_code: int, original_error: Exception | None = None):
        self.message = message
        self.status_code = status_code
        self.original_error = original_error
        super().__init__(self.message)