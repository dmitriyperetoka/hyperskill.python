from typing import Dict


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

    def __repr__(self) -> str:
        return self.service

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


SUB_QUEUES: Dict[str, SubQueue] = {
    'change_oil': SubQueue('Change oil', 2),
    'inflate_tires': SubQueue('Inflate tires', 5),
    'diagnostic': SubQueue('Get diagnostic', 30),
}


class PriorityQueue:
    """Multi-line queue with priority to the sub-queue of less waiting
    time per ticket.
    """

    def __init__(self, sub_queues: Dict[str, SubQueue] = None) -> None:
        if sub_queues is None:
            sub_queues = SUB_QUEUES
        self.sub_queues = sub_queues
        self.next_ticket_number = None

    def estimate_waiting_time(self, new_ticket_service: str) -> int:
        """Estimate waiting time before issuing a new ticket."""
        estimated_time = 0

        for service, sub_queue in self.sub_queues.items():
            estimated_time += sub_queue.estimate_waiting_time()

            if service == new_ticket_service:
                break

        return estimated_time

    def issue_ticket(self, service: str) -> int:
        """Add a new ticket to the corresponding sub-queue and return
        the ticket number.
        """
        ticket = Ticket()
        self.sub_queues[service].push(ticket)
        return ticket.number

    def process(self) -> None:
        """Select the next ticket to provide service to."""
        for service, sub_queue in sorted(
                self.sub_queues.items(),
                key=lambda item: item[1].minutes_per_ticket
        ):
            if not sub_queue.is_empty():
                self.next_ticket_number = sub_queue.pop().number
                break
