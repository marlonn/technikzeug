from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic

from .models import Artikel

# von schimpf kopiert - aufräumen!
from django.http import HttpResponse
from django.utils import timezone
from django import forms
from django.shortcuts import redirect, render_to_response, get_object_or_404
from django.template import RequestContext
from django.db.models import Q


class IndexView(generic.ListView):
    template_name = 'artikel/index.html'
    context_object_name = 'latest_artikel_list'

    def get_queryset(self):
        """Return the last fifteen published articles."""
        return Artikel.objects.order_by('-datum')[:50]

class DetailView(generic.DetailView):
    model = Artikel
    template_name = 'artikel/detail.html'

class SearchView(generic.ListView):
    template_name = 'artikel/search.html'
    context_object_name = 'artikel_list'

    def get_queryset(self):
        query = self.request.GET.get('q')
        #artikel_list.q = self.request.GET.get('q')
        if query:
            query_list = query.split()
            if len(query.split()) > 1:
                result = Artikel.objects.filter(
                            Q(tag__icontains=q) for q in query_list
                        ).order_by('-datum')
            else:
                result = Artikel.objects.filter(
                            Q(tags__icontains=query)
                        ).order_by('-datum')
        else:
            result = Artikel.objects.filter(
                        datum__lte=timezone.now()
                    ).order_by('-datum')[:80]
        return result
