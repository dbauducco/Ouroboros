from django.contrib import admin
from volunteer import models

from application import models as application_models


# Register your models here.
class FoodEventAdmin(admin.ModelAdmin):
    list_display = ("hacker", "timestamp", "meal", "restrictions")

    def has_add_permission(self, request, obj=None):
        return True

    def has_change_permission(self, request, obj=None):
        return True


class WorkshopEventAdmin(admin.ModelAdmin):
    list_display = ("hacker", "timestamp")

    def has_add_permission(self, request, obj=None):
        return True

    def has_change_permission(self, request, obj=None):
        return True


class ShiftAdmin(admin.ModelAdmin):
    list_display = ("start", "end")
    ordering = ("start",)

class VolunteerApplicationAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "phone_number")


admin.site.register(models.FoodEvent, FoodEventAdmin)
admin.site.register(models.WorkshopEvent, WorkshopEventAdmin)
admin.site.register(models.Shift, ShiftAdmin)
admin.site.register(models.VolunteerApplication, VolunteerApplicationAdmin)