from django.contrib import admin
from .models import MyUser, Member, Caregiver, Address, Job, Job_Application, Appointment

admin.site.register(MyUser)
admin.site.register(Member)
admin.site.register(Caregiver)
admin.site.register(Address)
admin.site.register(Job)
admin.site.register(Job_Application)
admin.site.register(Appointment)