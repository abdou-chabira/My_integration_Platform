from django.contrib import admin
from .models import ExternalIntegration

@admin.register(ExternalIntegration)
class ExternalIntegrationAdmin(admin.ModelAdmin):
    list_display = ('name', 'enabled')
