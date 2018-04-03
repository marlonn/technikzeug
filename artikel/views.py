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
        if query:
            query_list = query.split()
            # if len(query_list) > 1:
                # this branch does not work. it keeps throwing " 'Q' object has no attribute 'split'"
                # result = Artikel.objects.filter(
                #             Q(tags__icontains=item) for item in query_list
                #         ).order_by('-datum')
            # else
            result = Artikel.objects.filter(
                        Q(tags__icontains=query)  |
                        Q(titel__icontains=query) |
                        Q(text__icontains=query)
                    ).order_by('-datum')
        else:
            # result = Artikel.objects.filter(
            #             datum__lte=timezone.now()
            #         ).order_by('-datum')[:80]
            result = Artikel.objects.all().order_by('-datum')[:80]
        return result

# ------------------------ drf -------------------------------------------------
#~ from django.views.decorators.csrf import csrf_exempt
#~ from rest_framework.renderers import JSONRenderer
#~ from rest_framework.parsers import JSONParser
from artikel.serializers import ArtikelSerializer
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET', 'POST'])
def artikel_list(request, format=None):
    """List all entries, or create a new one"""
    if request.method == 'GET':
        artikel = Artikel.objects.all()
        serializer = ArtikelSerializer(artikel, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = ArtikelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET', 'PUT', 'DELETE'])
def artikel_detail(request, pk, format=None):
    """Retrieve, update or delete an entry."""
    try:
        artikel = Artikel.objects.get(pk=pk)
    except Artikel.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ArtikelSerializer(artikel)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ArtikelSerializer(artikel, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        artikel.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
