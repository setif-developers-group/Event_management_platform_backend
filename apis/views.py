from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import generics, filters, status
from app_models.models import Workshop, Speaker, Partner, Registration, Certificate
from .serializers import (WorkshopSerializer, SpeakerSerializer, 
                          PartnerSerializer, RegistrationSerializer, 
                          CertificateSerializer)
# Create your views here.
class HealthCheckView(generics.GenericAPIView):
    def get(self, request, *args, **kwargs):
        return Response({"status": "ok"}, status=status.HTTP_200_OK)

class WorkshopListCreateView(generics.ListAPIView):
    queryset = Workshop.objects.select_related('speaker', 'partner').all()
    serializer_class = WorkshopSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'description', 'speaker__name', 'partner__name'] 


class WorkshopDetailView(generics.RetrieveAPIView):
    queryset = Workshop.objects.all()
    serializer_class = WorkshopSerializer
    lookup_field = 'id'

class SpeakerListCreateView(generics.ListAPIView):
    queryset = Speaker.objects.select_related('partner').all()
    serializer_class = SpeakerSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'bio', 'partner__name']
class SpeakerDetailView(generics.RetrieveAPIView):
    queryset = Speaker.objects.all()
    serializer_class = SpeakerSerializer
    lookup_field = 'id'

class PartnerListCreateView(generics.ListAPIView):
    queryset = Partner.objects.all()
    serializer_class = PartnerSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'short_description']

class PartnerDetailView(generics.RetrieveAPIView):
    queryset = Partner.objects.all()
    serializer_class = PartnerSerializer
    lookup_field = 'id'
class RegistrationListCreateView(generics.CreateAPIView):
    queryset = Registration.objects.all()
    serializer_class = RegistrationSerializer


class CertificateDetailView(generics.RetrieveAPIView):
    queryset = Certificate.objects.all()
    serializer_class = CertificateSerializer
    lookup_field = 'id'