from django.contrib import admin
from login.models import User
# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'sex', 'c_time']

admin.site.register(User, UserAdmin)