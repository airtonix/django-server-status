from django.views.generic import TemplateView
from django.template.response import TemplateResponse
from django.http import HttpResponse, HttpResponseServerError

from .registry import plugins


class ServerStatusDashboard(TemplateView):
    template_name = "server_status/dashboard.html"

    def get_context_data(self, **kwargs):
        return {
            'Reports': plugins._registry.values()
        }
