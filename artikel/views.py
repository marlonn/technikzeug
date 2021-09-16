from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic

from .models import Artikel

# von schimpf kopiert - aufräumen!
from django.http import HttpResponse
from django.utils import timezone
from django import forms
from django.template import RequestContext
from django.db.models import Q


class IndexView(generic.ListView):
    template_name = 'artikel/index.html'
    context_object_name = 'latest_artikel_list'

    def get_queryset(self):
        """Return the last fifty published articles."""
        return Artikel.objects.order_by('-datum')[:50]

class DetailView(generic.DetailView):
    model = Artikel
    template_name = 'artikel/detail.html'

class SearchView(generic.ListView):
    template_name = 'artikel/search.html'
    context_object_name = 'artikel_list'

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            query_list = query.split()
            result = Artikel.objects.filter(
                        Q(tags__icontains=query)  |
                        Q(titel__icontains=query) |
                        Q(text__icontains=query)
                    ).order_by('-datum')
        else:
            result = Artikel.objects.all().order_by('-datum')[:80]
        return result

# ------------------------ drf -------------------------------------------------
from artikel.serializers import ArtikelSerializer
from rest_framework import generics
from rest_framework import permissions
from artikel.permissions import IsOwnerOrReadOnly

class ArtikelList(generics.ListCreateAPIView):
    queryset = Artikel.objects.all()
    serializer_class = ArtikelSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
        
class ArtikelDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                            IsOwnerOrReadOnly,)
    queryset = Artikel.objects.all()
    serializer_class = ArtikelSerializer
    
# ------------------------ user ------------------------------------------------
from django.contrib.auth.models import User
from artikel.serializers import UserSerializer

class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
