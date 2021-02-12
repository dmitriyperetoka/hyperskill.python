class PopFromEmptySubQueueError(Exception):
    """Tried to pop from an empty sub-queue."""

    def __init__(self, message='pop from empty sub-queue'):
        self.message = message

    def __str__(self):
        return self.message
