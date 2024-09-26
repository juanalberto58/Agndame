from django.contrib import admin
from .models import Appointment, Service, Worker, Category

admin.site.register(Appointment)
admin.site.register(Service)
admin.site.register(Worker)
admin.site.register(Category)
