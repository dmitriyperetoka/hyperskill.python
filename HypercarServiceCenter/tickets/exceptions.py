class PopFromEmptySubQueueError(Exception):
    """Tried to pop from an empty sub-queue."""

    def __str__(self):
        return 'pop from empty sub-queue'
