from django.contrib import admin
from .models import *

admin.site.register(Event)


# class EventAdmin(admin.ModelAdmin):
#     list_display = ('name', 'age', 'gender', 'contact')
#     search_fields = ('name', 'contact')
#     list_filter = ('gender',)

# admin.site.register(Event, EventAdmin)





# Register your models here.
