from django.urls import path, include
from . import views
urlpatterns = [
    path('health/', views.HealthCheckView.as_view(), name='health-check'),
    path('workshops/', views.WorkshopListView.as_view(), name='workshop-list-available-for-registration'),
    path('workshops/<int:id>/', views.WorkshopDetailView.as_view(), name='workshop-detail'),
    path('speakers/', views.SpeakerListView.as_view(), name='speaker-list-create'),
    path('speakers/<int:id>/', views.SpeakerDetailView.as_view(), name='speaker-detail'),
    path('partners/', views.PartnerListView.as_view(), name='partner-list-create'),
    path('partners/<int:id>/', views.PartnerDetailView.as_view(), name='partner-detail'),
    path('registrations/', views.RegistrationCreateView.as_view(), name='registration-list-create'),
    path('certificates/<int:id>/', views.CertificateDetailView.as_view(), name='certificate-detail'),
    path('attendances/', views.AttendanceCreateView.as_view(), name='attendance-list-create'),
]