from django.contrib import admin

# Register your models here.

from .models import *

admin.site.register(Utente)
admin.site.register(Categoria)
admin.site.register(Piatto)
admin.site.register(Ordinazione)