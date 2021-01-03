from typing import Dict, ItemsView, Union, ValuesView

from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.template.response import TemplateResponse
from django.views.generic import TemplateView, View

from .services import SubQueue, Queue

queue = Queue()


class WelcomeView(View):
    greeting = '<h2>Welcome to the Hypercar Service!</h2>'

    def get(self, request: HttpRequest) -> HttpResponse:  # noqa
        return HttpResponse(self.greeting)


class MenuView(TemplateView):
    template_name = 'menu.html'

    def get_context_data(self) -> Dict[str, ItemsView[str, SubQueue]]:
        return {'items': queue.sub_queues.items()}


class GetTicketView(TemplateView):
    template_name = 'get_ticket.html'

    def get_context_data(
            self,
            **kwargs: Dict[str, str]
    ) -> Dict[str, Union[str, int]]:
        context = super().get_context_data(**kwargs)
        service = context['service']
        context['waiting_time'] = queue.estimate_waiting_time(service)
        context['ticket_number'] = queue.issue_ticket(service)
        return context


class ProcessView(TemplateView):
    template_name = 'processing.html'

    def get_context_data(self) -> Dict[str, ValuesView[SubQueue]]:
        return {'sub_queues': queue.sub_queues.values()}

    def post(self, request: HttpRequest) -> TemplateResponse:
        queue.process()
        return self.get(request)


class NextView(TemplateView):
    template_name = 'next.html'

    def get_context_data(self) -> Dict[str, int]:
        return {'next_ticket_number': queue.next_ticket_number}
