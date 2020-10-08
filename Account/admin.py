from django.contrib import admin
from Account.models import Registration
# Register your models here.

class RegistrationAdmin(admin.ModelAdmin):
    list_display = ('first_name','last_name','mobile_number','email','password')
admin.site.register(Registration,RegistrationAdmin)
