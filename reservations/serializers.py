from rest_framework import serializers

from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

from users.models import Profile
from reservations.models import Reservation


User = get_user_model()


class ReservationCreateSerializer(serializers.Serializer):
    title = serializers.CharField(write_only=True)
    description = serializers.CharField(write_only=True)
    reserve_date = serializers.DateField(write_only=True)
    floor = serializers.IntegerField(write_only=True)
    start_time = serializers.TimeField(write_only=True)
    end_time = serializers.TimeField(write_only=True)
    
    
    def validate_time(self, reserve_date, start_time, end_time, floor):
        if start_time > end_time:
            raise serializers.ValidationError(_("The start time must precede the end time"))
        
        reservations = Reservation.objects.filter(reserve_date=reserve_date)
        
        for rev in reservations:
            if end_time <= rev.start_time and rev.end_time <= start_time:
                continue
            else:
                raise serializers.ValidationError(_("Already reserved"))
                
    
    def validate(self, data):
        if not data['title']:
            raise serializers.ValidationError(_("title required"))
        if not data['reserve_date']:
            raise serializers.ValidationError(_("reservation date required"))
        if not data['start_time']:
            raise serializers.ValidationError(_("start_time required"))
        if not data['end_time']:
            raise serializers.ValidationError(_("end_time required"))
        
        self.validate_time(
            data['reserve_date'],
            data['start_time'],
            data['end_time'],
            data['floor']
        )
        
        return data
    
    def create(self, validated_data):
        user = self.context['request'].user
        reservation = Reservation(
            title=validated_data['title'],
            description=validated_data['description'],
            reserve_date=validated_data['reserve_date'],
            floor=validated_data['floor'],
            start_time=validated_data['start_time'],
            end_time=validated_data['end_time'],
            booker=user,
        )
        
        return reservation
        