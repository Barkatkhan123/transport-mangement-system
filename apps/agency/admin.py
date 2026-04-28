from django.contrib import admin
from django.utils import timezone
from django.utils.html import format_html
from .models import Agency, Driver, Bus


@admin.register(Agency)
class AgencyAdmin(admin.ModelAdmin):
    list_display = ('name', 'manager', 'city', 'status', 'status_badge', 'created_at')
    list_editable = ('status',)
    list_filter = ('status', 'city', 'created_at')
    search_fields = ('name', 'manager__full_name', 'manager__email', 'registration_number')
    actions = ['approve_agencies', 'reject_agencies', 'suspend_agencies']
    readonly_fields = ('approved_at',)

    @admin.display(description='Status')
    def status_badge(self, obj):
        colors = {
            'pending': '#f59e0b',    # Amber
            'approved': '#10b981',   # Emerald
            'rejected': '#ef4444',   # Red
            'suspended': '#6b7280',  # Gray
        }
        color = colors.get(obj.status, '#374151')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 4px 10px; border-radius: 9999px; font-weight: bold; font-size: 11px; text-transform: uppercase;">{}</span>',
            color,
            obj.get_status_display()
        )

    @admin.action(description='Approve selected agencies')
    def approve_agencies(self, request, queryset):
        updated = queryset.update(status='approved', approved_at=timezone.now())
        self.message_user(request, f'{updated} agencies have been successfully approved.')

    @admin.action(description='Reject selected agencies')
    def reject_agencies(self, request, queryset):
        updated = queryset.update(status='rejected')
        self.message_user(request, f'{updated} agencies have been rejected.')

    @admin.action(description='Suspend selected agencies')
    def suspend_agencies(self, request, queryset):
        updated = queryset.update(status='suspended')
        self.message_user(request, f'{updated} agencies have been suspended.')


@admin.register(Driver)
class DriverAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'agency', 'license_number', 'status', 'experience_years')
    list_filter = ('status', 'agency')
    search_fields = ('full_name', 'license_number')


@admin.register(Bus)
class BusAdmin(admin.ModelAdmin):
    list_display = ('registration_number', 'agency', 'bus_type', 'total_seats', 'status')
    list_filter = ('bus_type', 'status', 'agency')
    search_fields = ('registration_number', 'model_name')
