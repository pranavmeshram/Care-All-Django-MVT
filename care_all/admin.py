from django.contrib import admin
from care_all.models import Elder, Youngster, CareRequest, Reviews

# Register your models here.



class YoungsterAdmin(admin.ModelAdmin):
    list_display = ("user", "name", "age", "elders_in_care")


class ElderAdmin(admin.ModelAdmin):
    list_display = ("user", "name", "status", "in_care")


class CareRequestAdmin(admin.ModelAdmin):
    list_display = ("sender", "requested_for")



admin.site.register(Youngster, YoungsterAdmin)
admin.site.register(Elder, ElderAdmin)
admin.site.register(CareRequest, CareRequestAdmin)
admin.site.register(Reviews)