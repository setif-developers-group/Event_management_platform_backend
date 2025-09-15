from django.urls import path, include
from . import views
urlpatterns = [
    path('health/', views.HealthCheckView.as_view(), name='health-check'),
    path('workshops/', views.WorkshopListCreateView.as_view(), name='workshop-list-create'),
    path('workshops/<int:id>/', views.WorkshopDetailView.as_view(), name='workshop-detail'),
    path('speakers/', views.SpeakerListCreateView.as_view(), name='speaker-list-create'),
    path('speakers/<int:id>/', views.SpeakerDetailView.as_view(), name='speaker-detail'),
    path('partners/', views.PartnerListCreateView.as_view(), name='partner-list-create'),
    path('partners/<int:id>/', views.PartnerDetailView.as_view(), name='partner-detail'),
    path('registrations/', views.RegistrationListCreateView.as_view(), name='registration-list-create'),
    path('certificates/<int:id>/', views.CertificateDetailView.as_view(), name='certificate-detail'),
]