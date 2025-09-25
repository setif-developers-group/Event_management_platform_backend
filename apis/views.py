from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import generics, filters, status, views
from rest_framework.permissions import IsAuthenticated
from app_models.models import Workshop, Speaker, Partner, Registration, Certificate, Attendance
from .serializers import (WorkshopSerializer, SpeakerSerializer, 
                          PartnerSerializer, RegistrationSerializer, 
                          CertificateSerializer,
                          AttendanceSerializer,WorkshopAllSerializer)
from .utils import get_registration_week_nuber, get_time_from_last_registration
from drf_spectacular.utils import extend_schema, OpenApiResponse
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
class RegistrationCreateView(generics.CreateAPIView):
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
        if Workshop.objects.filter(id=request.data['workshop']).first().week != get_registration_week_nuber():
            return Response({"error": "Registration is closed or didn't start yet"}, status=status.HTTP_400_BAD_REQUEST)
        return super().create(request, *args, **kwargs)



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
