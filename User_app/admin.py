from django.contrib import admin
# ---
from .models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "gender", "phone_number", "email")


admin.site.register(User, UserAdmin)