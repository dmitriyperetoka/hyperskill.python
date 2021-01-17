from typing import Dict, Tuple

from .exceptions import PopFromEmptySubQueueError


class Ticket:
    """Node-like object for linked list in SubQueue."""

    tickets_issued = 0

    def __new__(cls) -> 'Ticket':
        cls.tickets_issued += 1
        return object.__new__(cls)

    def __init__(self) -> None:
        self.number = Ticket.tickets_issued
        self.next = None


class SubQueue:
    """Linked list based queue with Ticket objects as nodes."""

    def __init__(self, service: str, minutes_per_ticket: int) -> None:
        self.minutes_per_ticket = minutes_per_ticket
        self.service = service
        self.length = 0
        self.head = None
        self.tail = None

    def is_empty(self) -> bool:
        """Check if the sub-queue is empty."""
        if self.length == 0:
            return True

        return False

    def push(self, ticket: Ticket) -> None:
        """Add new ticket to the sub-queue."""
        if self.is_empty():
            self.head = ticket
            self.tail = ticket
        else:
            self.tail.next = ticket
            self.tail = ticket

        self.length += 1

    def pop(self) -> Ticket:
        """Extract next ticket from the sub-queue."""
        if self.is_empty():
            raise PopFromEmptySubQueueError

        ticket = self.head
        self.length -= 1

        if self.is_empty():
            self.head, self.tail = None, None
        else:
            self.head = self.head.next

        return ticket

    def estimate_waiting_time(self) -> int:
        """Estimate time to serve all the tickets in the sub-queue."""
        return self.minutes_per_ticket * self.length


DEFAULT_SUB_QUEUES_PRESET: Dict[str, Tuple[str, int]] = {
    'change_oil': ('Change oil', 2),
    'inflate_tires': ('Inflate tires', 5),
    'diagnostic': ('Get diagnostic', 30),
}


class PriorityQueue:
    """Multi-line queue with priority to the sub-queue of less waiting
    time per ticket.
    """

    def __init__(self, preset: Dict[str, Tuple[str, int]] = None) -> None:
        if preset is None:
            preset = DEFAULT_SUB_QUEUES_PRESET

        self.sub_queues = {
            link: SubQueue(*args) for link, args in preset.items()
        }
        self.next_ticket_number = None

    def estimate_waiting_time(self, service: str) -> int:
        """Estimate waiting time before issuing a new ticket."""
        max_minutes_per_ticket = self.sub_queues[service].minutes_per_ticket
        estimated_time = 0

        for sub_queue in self.sub_queues.values():
            if sub_queue.minutes_per_ticket <= max_minutes_per_ticket:
                estimated_time += sub_queue.estimate_waiting_time()

        return estimated_time

    def issue_ticket(self, service: str) -> Tuple[int, int]:
        """Add a new ticket to the corresponding sub-queue and return
        the ticket number.
        """
        estimated_time = self.estimate_waiting_time(service)
        ticket = Ticket()
        self.sub_queues[service].push(ticket)
        return ticket.number, estimated_time

    def get_next_sub_queue(self) -> SubQueue:
        """Return the next sub-queue to extract ticket from."""
        sorted_sub_queues = sorted(
            self.sub_queues.values(),
            key=lambda value: value.minutes_per_ticket
        )

        for sub_queue in sorted_sub_queues:
            if not sub_queue.is_empty():
                return sub_queue

    def process(self) -> None:
        """Extract the next ticket to provide service to."""
        next_sub_queue = self.get_next_sub_queue()

        if next_sub_queue:
            self.next_ticket_number = next_sub_queue.pop().number
