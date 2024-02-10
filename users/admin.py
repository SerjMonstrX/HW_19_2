from django.contrib import admin
from users.models import User


@admin.register(User)
class Userdmin(admin.ModelAdmin):
    list_display = ('email', 'is_verified', )
    list_filter = ('is_verified',)
    search_fields = ('email', 'is_verified', )