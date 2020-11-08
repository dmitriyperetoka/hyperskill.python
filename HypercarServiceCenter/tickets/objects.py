from collections import deque


SERVICES = {
    'change_oil': {
        'service_queue': deque(),
        'minutes_per_ticket': 2,
        'text': 'Change oil'
    },
    'inflate_tires': {
        'service_queue': deque(),
        'minutes_per_ticket': 5,
        'text': 'Inflate tires'
    },
    'diagnostic': {
        'service_queue': deque(),
        'minutes_per_ticket': 30,
        'text': 'Get diagnostic'
    }
}


class Queue:
    def __init__(self):
        self.services = SERVICES
        self.last_issued_ticket = 0
        self.served_next_ticket = None

    def estimate_waiting_time(self, service):
        estimated_time = 0

        for q in self.services:
            if (
                    self.services[q]['minutes_per_ticket']
                    <= self.services[service]['minutes_per_ticket']
            ):
                estimated_time += (
                        self.services[q]['minutes_per_ticket']
                        * len(self.services[q]['service_queue'])
                )

        return estimated_time

    def issue_ticket(self, service):
        if service in self.services:
            self.last_issued_ticket += 1
            self.services[service]['service_queue'].appendleft(
                self.last_issued_ticket
            )
            return self.last_issued_ticket

    def process(self):
        queued_services = tuple(
            q for q in self.services if self.services[q]['service_queue']
        )

        if queued_services:
            next_service = min(
                queued_services,
                key=lambda x: self.services[x]['minutes_per_ticket']
            )
            self.served_next_ticket = (
                self.services[next_service]['service_queue'].pop()
            )
        else:
            self.served_next_ticket = None
