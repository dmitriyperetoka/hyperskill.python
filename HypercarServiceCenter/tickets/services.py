class Ticket:
    tickets_issued = 0

    def __new__(cls):
        cls.tickets_issued += 1
        return object.__new__(cls)

    def __init__(self):
        self.number = Ticket.tickets_issued
        self.next = None


class SubQueue:
    def __init__(self, service, minutes_per_ticket):
        self.minutes_per_ticket = minutes_per_ticket
        self.service = service
        self.length = 0
        self.head = None
        self.tail = None

    def is_empty(self):
        if self.length == 0:
            return True

        return False

    def enqueue(self, ticket):
        if self.is_empty():
            self.head = ticket
            self.tail = ticket
        else:
            self.tail.next = ticket
            self.tail = ticket

        self.length += 1

    def dequeue(self):
        ticket_number = self.head.number
        self.length -= 1

        if self.is_empty():
            self.head, self.tail = None, None
        else:
            self.head = self.head.next

        return ticket_number

    def estimate_waiting_time(self):
        return self.minutes_per_ticket * self.length


class Queue:
    def __init__(self):
        self.next_ticket_number = None
        self.sub_queues = {
            'change_oil': SubQueue('Change oil', 2),
            'inflate_tires': SubQueue('Inflate tires', 5),
            'diagnostic': SubQueue('Get diagnostic', 30),
        }

    def issue_ticket(self, service):
        ticket = Ticket()
        self.sub_queues[service].enqueue(ticket)
        return ticket.number

    def process(self):
        for sub_que in self.sub_queues.values():
            if not sub_que.is_empty():
                self.next_ticket_number = sub_que.dequeue()
                break

    def estimate_waiting_time(self, new_ticket_service):
        estimated_time = 0

        for service, sub_queue in self.sub_queues.items():
            estimated_time += sub_queue.estimate_waiting_time()

            if service == new_ticket_service:
                break

        return estimated_time
