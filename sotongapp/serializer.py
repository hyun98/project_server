from time import strptime, mktime

from rest_framework import serializers
from sotongapp.models import Organ, Information


class OrganSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organ
        fields = ('name')


class InfoSerializer(serializers.ModelSerializer):
    name = serializers.ReadOnlyField(source='organ.name')
    urlname = serializers.ReadOnlyField(source='organ.urlname')

    class Meta:
        model = Information
        fields = ('name', 'urlname', 'temp', 'day', 'time')
    
    def to_representation(self, instance):
        info = super().to_representation(instance)
        organ_name = info["name"]
        temp_list = []
        
        times = strptime(str(info["day"]) + " " + str(info["time"]), '%Y-%m-%d %H:%M:%S')
        utc_now = mktime(times) * 1000
        temp_list.append([utc_now, info['temp']])

        data = {
            'name': organ_name,
            'temp': temp_list
        }
        
        return data