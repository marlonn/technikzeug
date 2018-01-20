from django.contrib import admin
from .models import Artikel

class ArtikelAdmin(admin.ModelAdmin):
#    fields = ('titel', 'tags', 'datum')
    search_fields = ('titel','tags')
    list_display = ('titel', 'datum', 'tags')

admin.site.register(Artikel, ArtikelAdmin)
