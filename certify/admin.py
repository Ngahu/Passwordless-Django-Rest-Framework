from django.contrib import admin

# Register your models here.
from .models import CallbackToken



class CallbackTokenAdmin(admin.ModelAdmin):
    readonly_fields = [
        'created_at',
         'key',
         'is_active',
         'is_invalidated',
         ]#user
    list_display = [
        'created_at',
        'user',
        'key',
        'is_active'
    ]
    search_fields = [
        'user',
        'key',
    ]



admin.site.register(CallbackToken,CallbackTokenAdmin)
     
