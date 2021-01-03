class Ticket:
    tickets_issued = 0

    def __new__(cls):
        cls.tickets_issued += 1
        return object.__new__(cls)

    def __init__(self) -> None:
        self.number = Ticket.tickets_issued
        self.next = None


class SubQueue:
    def __init__(self, service: str, minutes_per_ticket: int) -> None:
        self.minutes_per_ticket = minutes_per_ticket
        self.service = service
        self.length = 0
        self.head = None
        self.tail = None

    def is_empty(self) -> bool:
        if self.length == 0:
            return True

        return False

    def push(self, ticket: Ticket) -> None:
        if self.is_empty():
            self.head = ticket
            self.tail = ticket
        else:
            self.tail.next = ticket
            self.tail = ticket

        self.length += 1

    def pop(self) -> Ticket:
        ticket = self.head
        self.length -= 1

        if self.is_empty():
            self.head, self.tail = None, None
        else:
            self.head = self.head.next

        return ticket

    def estimate_waiting_time(self) -> int:
        return self.minutes_per_ticket * self.length


class Queue:
    def __init__(self) -> None:
        self.next_ticket_number = None
        self.sub_queues = {
            'change_oil': SubQueue('Change oil', 2),
            'inflate_tires': SubQueue('Inflate tires', 5),
            'diagnostic': SubQueue('Get diagnostic', 30),
        }

    def issue_ticket(self, service: str) -> int:
        ticket = Ticket()
        self.sub_queues[service].push(ticket)
        return ticket.number

    def process(self) -> None:
        for sub_que in self.sub_queues.values():
            if not sub_que.is_empty():
                self.next_ticket_number = sub_que.pop().number
                break

    def estimate_waiting_time(self, new_ticket_service: str) -> int:
        estimated_time = 0

        for service, sub_queue in self.sub_queues.items():
            estimated_time += sub_queue.estimate_waiting_time()

            if service == new_ticket_service:
                break

        return estimated_time
