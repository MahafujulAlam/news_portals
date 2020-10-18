from django.contrib import admin
from UserRole.models import Role, ContentType
# Register your models here.

class RoleAdmin(admin.ModelAdmin):
    list_display = ('id', 'role')
admin.site.register(Role, RoleAdmin)

class ContentTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'type')
admin.site.register(ContentType, ContentTypeAdmin)
