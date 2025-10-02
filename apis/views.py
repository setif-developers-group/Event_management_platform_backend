from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import generics, filters, status, views
from rest_framework.permissions import IsAuthenticated
from app_models.models import Workshop, Speaker, Partner, Registration, Certificate, Attendance
from .serializers import (WorkshopSerializer, SpeakerSerializer, 
                          PartnerSerializer, RegistrationSerializer, 
                          CertificateSerializer,
                          AttendanceSerializer,WorkshopAllSerializer,
                          WorkshopSimpleSerializer, RegistrationCreateSerializer, EmailConfirmationSerializer)
from .utils import get_registration_week_nuber, get_time_from_last_registration, is_workshop_finished, validate_email_workshop
from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework.throttling import UserRateThrottle
from .throttles import (RegisterThrottleMin, RegisterThrottleHour, RegisterThrottleHalfDay, RegisterThrottleDay, 
                        LoginThrottle, RefreshThrottle, LoginUserNameThrottle,
                        ConfirmEmailDayThrottle, ConfirmEmailHourThrottle, ConfirmEmailThrottle)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
# Create your views here.


class HealthCheckView(views.APIView):

    def get(self, request, *args, **kwargs):
        return Response({"status": "ok"}, status=status.HTTP_200_OK)

class WorkshopListView(generics.ListAPIView):
    queryset = Workshop.objects.all()
    serializer_class = WorkshopSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'description', 'speakers__name', 'partner__name'] 

    def get_queryset(self):
        return super().get_queryset().filter(week=get_registration_week_nuber())

class WorkshopListAllView(generics.ListAPIView):
    queryset = Workshop.objects.all()
    serializer_class = WorkshopAllSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'description', 'speakers__name', 'partner__name'] 


class WorkshopDetailView(generics.RetrieveAPIView):
    queryset = Workshop.objects.all()
    serializer_class = WorkshopSerializer
    lookup_field = 'id'

class SpeakerListView(generics.ListAPIView):

    queryset = Speaker.objects.select_related('partner').all()
    serializer_class = SpeakerSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'bio', 'partner__name']
class SpeakerDetailView(generics.RetrieveAPIView):
    throttle_classes = [UserRateThrottle]
    queryset = Speaker.objects.all()
    serializer_class = SpeakerSerializer
    lookup_field = 'id'

class PartnerListView(generics.ListAPIView):

    queryset = Partner.objects.all()
    serializer_class = PartnerSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'short_description']

class PartnerDetailView(generics.RetrieveAPIView):

    queryset = Partner.objects.all()
    serializer_class = PartnerSerializer
    lookup_field = 'id'

class RegistrationCreateView(views.APIView):
    throttle_classes = [RegisterThrottleMin, RegisterThrottleHour, RegisterThrottleHalfDay, RegisterThrottleDay]
    queryset = Registration.objects.all()
    serializer_class = RegistrationCreateSerializer
    
    def post(self, request):
        serializer = RegistrationCreateSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            email = data.get('email', '')
            workshop_id = data.get('workshop_id', '')
            validation_error = validate_email_workshop(email, workshop_id)
            if validation_error:
                return Response({"error": validation_error}, status=status.HTTP_400_BAD_REQUEST)
            msg = serializer.save()
            return Response({"status": msg}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EmailConfirmationView(views.APIView):

    def post(self, request):
        serializer = EmailConfirmationSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data.get('token',{})
            email = data.token.get('email')
            workshop_id = data.get('workshop_id')
            validation_error = validate_email_workshop(email, workshop_id)
            if validation_error:
                return Response({"error": validation_error}, status=status.HTTP_400_BAD_REQUEST)
            msg = serializer.save()
            return Response({"status": msg}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




    '''class RegistrationCreateView(generics.CreateAPIView):
    throttle_classes = [RegisterThrottleMin, RegisterThrottleHour, RegisterThrottleHalfDay, RegisterThrottleDay]
    queryset = Registration.objects.all()
    serializer_class = RegistrationSerializer
    @extend_schema(
        responses={
            
            400: OpenApiResponse(
                response={"error": "Registration is closed or didn't start yet"},
                description="Registration not allowed outside the correct week."
            ),
        }
    )
    def create(self, request, *args, **kwargs):
        email = request.data.get('email', '')
        if email and is_temp_email(email):
            return Response({
                'error': 'boot detected not alowed'
            }, status=400)

        # Block temp emails in message content
        if Workshop.objects.filter(id=request.data['workshop']).first().week != get_registration_week_nuber():
            return Response({"error": "Registration is closed or didn't start yet"}, status=status.HTTP_400_BAD_REQUEST)
        return super().create(request, *args, **kwargs)
'''
class CertificateListView(generics.ListAPIView):

    permission_classes = [IsAuthenticated]
    queryset = Certificate.objects.all()
    serializer_class = CertificateSerializer

class GenerateCertificatesView(views.APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, workshop, *args, **kwargs):
        workshop_instance = Workshop.objects.filter(id=workshop).first()
        if workshop_instance is None:
            return Response({"error": "Workshop not found"}, status=status.HTTP_404_NOT_FOUND)
        if not is_workshop_finished(workshop_instance):
            return Response({"error": "Workshop is not finished yet"}, status=status.HTTP_400_BAD_REQUEST)
        registration = Registration.objects.filter(workshop=workshop_instance, confirmed=True)
        create_counter = 0
        for reg in registration:
            if reg.attendances.count() >= (workshop_instance.sessions * 0.8) and not reg.certificate:
                Certificate.objects.create(registration=reg)
                create_counter += 1
        return Response({"status": f"{create_counter} certificates created"}, status=status.HTTP_200_OK)

class CertificateDetailView(generics.RetrieveAPIView):
    queryset = Certificate.objects.all()
    serializer_class = CertificateSerializer
    lookup_field = 'id'


class AttendanceCreateView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer

    def create(self, request, *args, **kwargs):
        if (last_attendance := Attendance.objects.filter(registration=request.data['registration']).last()) is not None:
            if get_time_from_last_registration(last_attendance) < 12:
                return Response({"error": "attendance already exists for this day"}, status=status.HTTP_409_CONFLICT)
        return super().create(request, *args, **kwargs)


class LoginView(TokenObtainPairView):
    throttle_classes = [LoginThrottle, LoginUserNameThrottle]

class RefreshView(TokenRefreshView):
    throttle_classes = [RefreshThrottle]