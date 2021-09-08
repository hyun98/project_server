from django.contrib import admin

from activity.models import Activity, ActivityDetail, ActivityDetailImage


admin.site.register(Activity)
admin.site.register(ActivityDetail)
admin.site.register(ActivityDetailImage)