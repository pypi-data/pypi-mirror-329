class InvalidMaxProgress(Exception):
    def __init__(self, max_progress):
        self.maxprogress = max_progress
        self.message = f"'{max_progress}' is not valid number for max_progress"
        super().__init__(self.message)