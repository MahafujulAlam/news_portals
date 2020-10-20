from django.contrib import admin
from UserRole.models import Role
# Register your models here.

class RoleAdmin(admin.ModelAdmin):
    list_display = ('id', 'role')
admin.site.register(Role, RoleAdmin)
