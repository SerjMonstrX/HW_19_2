from django.contrib import admin
from users.models import User


@admin.register(User)
class Userdmin(admin.ModelAdmin):
    list_display = ('email', 'is_active', )
    list_filter = ('is_active',)
    search_fields = ('email', 'is_active', )