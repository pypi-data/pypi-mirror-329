class PromptNotFoundException(Exception):
    def __init__(self, message: str = "Prompt not found!", error_code: int = 404) -> None:
        super().__init__(message)
        self.message = message
        self.error_code = error_code
