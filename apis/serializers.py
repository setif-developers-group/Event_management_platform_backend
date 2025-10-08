from rest_framework import serializers
from app_models.models import Workshop, Speaker, Partner, Registration, Certificate, Attendance, AttendanceType
from django_recaptcha.fields import ReCaptchaField as BaseReCaptchaField
from .utils import sent_email_confirmation_email, create_email_confirmation_token, decode_email_confirmation_token
import jwt
from decouple import config

class ReCaptchaField(serializers.CharField):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.write_only = True
        self.recaptcha = BaseReCaptchaField()

    def to_internal_value(self, data):
        value = super().to_internal_value(data)
        # Validate using django-recaptcha's validation
        self.recaptcha.clean(value)
        return value
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

class RegistrationCreateSerializer(serializers.Serializer):
    workshop = serializers.PrimaryKeyRelatedField(queryset=Workshop.objects.all())
    first_name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=100)    
    email = serializers.EmailField()
    phone_number = serializers.CharField(max_length=10, min_length=10)
    attendance_type = serializers.ChoiceField(choices=AttendanceType.choices)
    captcha = ReCaptchaField(required=False)

    def validate(self, data):
        request = self.context.get('request')
        
        # Check if it's a chatbot request
        is_chatbot = (request.headers.get('SSL-Chatbot-Key') == config('SSL_CHATBOT_KEY', default='your-secret-key'))
        if is_chatbot:
            # If it's a chatbot request, remove captcha validation
            data.pop('captcha', None)
            return data
            
        # The captcha field will handle validation through the ReCaptchaField class
        return data
        

    def save(self, **kwargs):
        data = self.validated_data
        workshop = data.pop('workshop')
        data['workshop_id'] = workshop.id
        data['workshop_title'] = workshop.title
        data['workshop_date'] = workshop.date
        payload = create_email_confirmation_token(data)
        sent_email_confirmation_email(data, payload)
        return f'A confirmation email has been sent to {data.get("email")}. Please check your inbox to confirm your registration.'
    
class EmailConfirmationSerializer(serializers.Serializer):
    token = serializers.CharField()
    captcha = ReCaptchaField(required=True)
    def validate(self, data):
        try:
            payload = decode_email_confirmation_token(data.get('token'))
            print('payload', payload)
            return payload
        except jwt.ExpiredSignatureError as e:
            raise serializers.ValidationError(str(e))
        except jwt.InvalidTokenError as e:
            raise serializers.ValidationError(str(e))
        except Exception as e:
            raise serializers.ValidationError(str(e))

    def save(self, **kwargs):
        payload = self.validated_data   
        email = payload.get('email')
        workshop_id = payload.get('workshop')
        first_name = payload.get('first_name')
        last_name = payload.get('last_name')
        phone_number = payload.get('phone_number')
        attendance_type = payload.get('attendance_type')
        registration = Registration.objects.filter(email=email, workshop_id=workshop_id).first()
        if registration:
            return f'Your email has already been confirmed for {registration.workshop.title}.'
        else:
            registration = Registration.objects.create(
                workshop_id=workshop_id,
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone_number=phone_number,
                attendance_type=attendance_type,
                confirmed=False
            )
            return 'Your email has been confirmed and registration completed successfully.'

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