from django.contrib import admin
from sotongapp.models import Information, Organ


class OrganAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'urlname'
    )
    list_display_links = (
        'name', 'urlname'
    )

class InformationAdmin(admin.ModelAdmin):
    list_display = (
        'get_organ_name', 'temp', 'day', 'time'
    )
    list_display_links = (
        'get_organ_name', 'temp', 'day', 'time'
    )
    list_filter = (
        'day', 'organ__name',
    )
    
    def get_organ_name(self, obj):
        return obj.organ.name
    get_organ_name.admin_order_field = "organ"
    get_organ_name.short_description = "기관명"
    

admin.site.register(Organ, OrganAdmin)
admin.site.register(Information, InformationAdmin)