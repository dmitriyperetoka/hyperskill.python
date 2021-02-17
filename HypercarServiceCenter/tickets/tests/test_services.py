from django.test import TestCase


class TicketsServicesTest(TestCase):
    def check_queue_state(self, change_oil, inflate_tires, diagnostic):
        response = self.client.get('/processing')
        sub_queues = response.context.get('sub_queues')
        items = [
            (sub_queue.service, sub_queue.length) for sub_queue in sub_queues
        ]
        expected_items = [
            ('Change oil', change_oil), ('Inflate tires', inflate_tires),
            ('Get diagnostic', diagnostic),
        ]

        with self.subTest():
            self.assertEqual(items, expected_items)

    def check_issue_ticket(self, service, ticket_number, waiting_time):
        response = self.client.get(f'/get_ticket/{service}/')

        with self.subTest():
            self.assertEqual(
                response.context.get('ticket_number'), ticket_number
            )

        with self.subTest():
            self.assertEqual(
                response.context.get('waiting_time'), waiting_time
            )

    def check_next_ticket_number(self, next_ticket_number):
        response = self.client.get('/next/')

        with self.subTest():
            self.assertEqual(
                response.context.get('next_ticket_number'), next_ticket_number
            )

    def test_queue_behaviour(self):
        self.check_queue_state(0, 0, 0)
        self.check_next_ticket_number(None)
        self.check_issue_ticket('inflate_tires', 1, 0)
        self.check_queue_state(0, 1, 0)
        self.check_next_ticket_number(None)
        self.check_issue_ticket('change_oil', 2, 0)
        self.check_queue_state(1, 1, 0)
        self.check_next_ticket_number(None)
        self.check_issue_ticket('change_oil', 3, 2)
        self.check_queue_state(2, 1, 0)
        self.check_next_ticket_number(None)
        self.client.post('/processing')
        self.check_queue_state(1, 1, 0)
        self.check_next_ticket_number(2)
        self.check_issue_ticket('change_oil', 4, 2)
        self.check_queue_state(2, 1, 0)
        self.check_next_ticket_number(2)
        self.check_issue_ticket('diagnostic', 5, 9)
        self.check_queue_state(2, 1, 1)
        self.check_next_ticket_number(2)
        self.client.post('/processing')
        self.check_queue_state(1, 1, 1)
        self.check_next_ticket_number(3)
        self.check_issue_ticket('inflate_tires', 6, 7)
        self.check_queue_state(1, 2, 1)
        self.check_next_ticket_number(3)
        self.client.post('/processing')
        self.check_queue_state(0, 2, 1)
        self.check_next_ticket_number(4)
        self.client.post('/processing')
        self.check_queue_state(0, 1, 1)
        self.check_next_ticket_number(1)
        self.client.post('/processing')
        self.check_queue_state(0, 0, 1)
        self.check_next_ticket_number(6)
        self.client.post('/processing')
        self.check_queue_state(0, 0, 0)
        self.check_next_ticket_number(5)
        self.client.post('/processing')
        self.check_queue_state(0, 0, 0)
        self.check_next_ticket_number(5)
