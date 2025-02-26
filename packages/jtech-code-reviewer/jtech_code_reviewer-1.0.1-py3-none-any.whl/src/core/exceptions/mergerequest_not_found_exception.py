class MergeRequestNotFoundException(Exception):
    def __init__(self, message: str, error_code: int = 404):
        self.message = message
        super().__init__(self.message)
        self.error_code = error_code
