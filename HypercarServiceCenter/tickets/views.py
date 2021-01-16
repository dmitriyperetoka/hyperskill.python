from typing import Dict, ItemsView, Union, ValuesView

from django.http.request import HttpRequest
from django.http.response import HttpResponse, HttpResponseNotFound
from django.template.response import TemplateResponse
from django.views.generic import TemplateView, View

from .services import PriorityQueue, SubQueue

queue = PriorityQueue()


class WelcomeView(View):
    """Display greeting message."""

    greeting_message = '<h2>Welcome to the Hypercar Service!</h2>'

    def get(self, request: HttpRequest) -> HttpResponse:  # noqa
        return HttpResponse(self.greeting_message)


class MenuView(TemplateView):
    """Display menu page."""

    template_name = 'menu.html'

    def get_context_data(self) -> Dict[str, ItemsView[str, SubQueue]]:
        return {'items': queue.sub_queues.items()}


class GetTicketView(TemplateView):
    """Issue new ticket and display its number and estimated
    waiting time.
    """

    template_name = 'get_ticket.html'

    def get_context_data(self, service: str) -> Dict[str, Union[int, str]]:
        ticket_number, waiting_time = queue.issue_ticket(service)
        return {'ticket_number': ticket_number, 'waiting_time': waiting_time}

    def get(self, request, **kwargs: Dict[str, str]) -> (
            Union[HttpResponse, HttpResponseNotFound]
    ):
        if kwargs.get('service') in queue.sub_queues.keys():
            return super().get(request, **kwargs)
        else:
            return HttpResponseNotFound()


class ProcessingView(TemplateView):
    """Display the operator menu and process the next ticket."""

    template_name = 'processing.html'

    def get_context_data(self) -> Dict[str, ValuesView[SubQueue]]:
        return {'sub_queues': queue.sub_queues.values()}

    def post(self, request: HttpRequest) -> TemplateResponse:
        queue.process()
        return self.get(request)


class NextView(TemplateView):
    """Display the page showing which ticket is next to serve."""

    template_name = 'next.html'

    def get_context_data(self) -> Dict[str, Union[None, int]]:
        return {'next_ticket_number': queue.next_ticket_number}
