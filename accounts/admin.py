from django.contrib import admin
from .models import Profile

# Register your models here.

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'address', 'bio', 'profile_picture')
    search_fields = ('user__username', 'phone', 'address', 'bio')
    list_filter = ('user', 'phone')
    ordering = ('user', 'phone')

