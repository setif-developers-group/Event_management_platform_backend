from rest_framework import serializers
from app_models.models import Workshop, Speaker, Partner, Registration, Certificate, Attendance

class WorkshopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workshop
        fields = '__all__'


class SpeakersNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Speaker
        fields = ['name']


class WorkshopAllSerializer(serializers.ModelSerializer):
    # add only the names of speakers
    speakers = SpeakersNameSerializer(many=True, read_only=True)

    class Meta:
        model = Workshop
        fields = '__all__'
        
    


class SpeakerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Speaker
        fields = '__all__'


class PartnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Partner
        fields = '__all__'


class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Registration
        fields = '__all__'
        read_only_fields = ['registration_date', 'confirmed']


class CertificateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certificate
        fields = '__all__'

class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = '__all__'