from rest_framework import serializers
from app_models.models import Workshop, Speaker, Partner, Registration, Certificate, Attendance

class WorkshopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workshop
        fields = '__all__'


class SpeakersNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Speaker
        fields = ['name', 'contact']

class PartnerNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Partner
        fields = ['name']

class WorkshopAllSerializer(serializers.ModelSerializer):
    # add only the names of speakers
    speakers = SpeakersNameSerializer(many=True, read_only=True)
    partner = PartnerNameSerializer(read_only=True)
    class Meta:
        model = Workshop
        fields = '__all__'
        
    


class SpeakerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Speaker
        fields = '__all__'


class PartnerSerializer(serializers.ModelSerializer):
    logo = serializers.URLField(source='logo.url', read_only=True)
    class Meta:
        model = Partner
        fields = '__all__'


class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Registration
        fields = '__all__'
        read_only_fields = ['registration_date', 'confirmed']

class WorkshopSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workshop
        fields = ['id', 'title', 'date', 'duration']
class CertificateSerializer(serializers.ModelSerializer):
    workshop = WorkshopSimpleSerializer(source='registration.workshop', read_only=True)
    registration_info = RegistrationSerializer(source='registration', read_only=True)
    class Meta:
        model = Certificate
        fields = '__all__'

class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = '__all__'