from django.contrib import admin
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from activity.models import Activity, ActivityDetail, ActivityDetailImage


# admin.site.register(Activity)
# admin.site.register(ActivityDetail)
# admin.site.register(ActivityDetailImage)



class ActivityDetailImageInline(admin.StackedInline):
    model = ActivityDetailImage
    can_delete = False
    verbose_name_plural = "activity_detail_images"
    
class ActivityDetailInline(admin.StackedInline):
    model = ActivityDetail
    can_delete = False
    verbose_name_plural = "activity_detail"

class ActivityInline(admin.StackedInline):
    model = Activity
    can_delete = False
    verbose_name_plural = "activity"



@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    ordering = ('-date', )
    list_display = (
        'get_thumbnail_image', 'title', 'description', 'date',
    )
    list_display_links = (
        'get_thumbnail_image', 'title', 'description', 'date',
    )
    search_fields = ('date', 'title', )
    list_filter = ('title', )
    
    inlines = (ActivityDetailInline, )
    
    def get_thumbnail_image(self, obj):
        image = obj.thumbnail
        
        if not image:
            return ''
        return mark_safe(f'<img src="{image.url}" style="width: 150px;">')
    get_thumbnail_image.short_description = _('Thumbnail Image')


@admin.register(ActivityDetail)
class ActivityDetailAdmin(admin.ModelAdmin):
    ordering = ('title', )
    list_display = (
        'get_thumbnail_image', 'activity', 'title', 'description',
    )
    list_display_links = (
        'get_thumbnail_image', 'activity', 'title', 'description',
    )
    search_fields = ('title', 'activity__title')
    list_filter = ('activity__title', )
    
    inlines = (ActivityDetailImageInline, )
    
    def get_thumbnail_image(self, obj):
        image = obj.image
        
        if not image:
            return ''
        return mark_safe(f'<img src="{image.url}" style="width: 150px;">')
    get_thumbnail_image.short_description = _('Images')
    
    

@admin.register(ActivityDetailImage)
class ActivityDetailImageAdmin(admin.ModelAdmin):
    ordering = ('activity_detail__title', )
    list_display = (
        'get_thumbnail_image', 'order', 'activity_detail',
    )
    list_display_links = (
        'get_thumbnail_image', 'order', 'activity_detail',
    )
    search_fields = ('date', 'activity_detail__title', )
    list_filter = ('activity_detail__title', )

    def get_thumbnail_image(self, obj):
        image = obj.image
        
        if not image:
            return ''
        return mark_safe(f'<img src="{image.url}" style="width: 150px;">')
    get_thumbnail_image.short_description = _('Images')