from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.db import connection

from .models import Artikel


class IndexView(generic.ListView):
    template_name = 'artikel/index.html'
    context_object_name = 'latest_artikel_list'

    def get_queryset(self):
        """Return the last fifteen published articles."""
        return Artikel.objects.order_by('-datum')[:50]

class DetailView(generic.DetailView):
    model = Artikel
    template_name = 'artikel/detail.html'
