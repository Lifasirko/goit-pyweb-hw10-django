from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Tag, Note

# Register your models here.
admin.site.register(Tag)
admin.site.register(Note)
