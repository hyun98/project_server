from rest_framework import serializers

from activity.models import ActivityDetail

class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityDetail
        fields = (
            'id', 'filename',
        )