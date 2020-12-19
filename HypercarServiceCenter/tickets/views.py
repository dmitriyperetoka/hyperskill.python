from django.http.response import HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView, View

from .services import Queue

queue = Queue()


class WelcomeView(View):
    greeting = '<h2>Welcome to the Hypercar Service!</h2>'

    def get(self, request):  # noqa
        return HttpResponse(self.greeting)


class MenuView(TemplateView):
    template_name = 'menu.html'

    def get_context_data(self):
        context = super().get_context_data()
        context['items'] = queue.sub_queues.items()
        return context


class GetTicketView(TemplateView):
    template_name = 'get_ticket.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        service = context['service']
        context['waiting_time'] = queue.estimate_waiting_time(service)
        context['ticket_number'] = queue.issue_ticket(service)
        return context


class ProcessingView(TemplateView):
    template_name = 'processing.html'

    def get_context_data(self):
        context = super().get_context_data()
        context['sub_queues'] = queue.sub_queues.values()
        return context

    def post(self, request):
        queue.process()
        return render(
            request,
            self.template_name,
            self.get_context_data()
        )


class NextView(TemplateView):
    template_name = 'next.html'

    def get_context_data(self):
        context = super().get_context_data()
        context['next_ticket_number'] = queue.next_ticket_number
        return context
