from django.views.generic import ListView
from .models import Datalog

class DashboardView(ListView):
    model = Datalog
    template_name = "dashboard/index.html"
    context_object_name = 'datalog_list'
