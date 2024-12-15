from django.urls import path
from .views import (
    EventListView,
    EventCreateView,
    EventDetailView,
    EventUpdateView,
    EventDeleteView,
    participant_list,
    participant_create,
    participant_update,
    participant_delete,
    send_email,  # Use send_email here instead of send-email
    generate_qr_code,
    event_statistique,
    text_to_speech,
    google_api_request,
    generate_image,
    chat_with_api,
    analyze_face,
)

urlpatterns = [
    path('', EventListView.as_view(), name='event_list'),  # This handles /events/
    path('create/', EventCreateView.as_view(), name='event_create'),  # This handles /events/create/
    path('<int:pk>/', EventDetailView.as_view(), name='event_detail'),
    path('<int:pk>/update/', EventUpdateView.as_view(), name='event_update'),
    path('<int:pk>/delete/', EventDeleteView.as_view(), name='event_delete'),
    

    # Participant URLs
    path('<int:event_id>/participants/', participant_list, name='participant_list'),
    path('<int:event_id>/participants/create/', participant_create, name='participant_create'),
    path('<int:event_id>/participants/google-api-request/', google_api_request, name='google_api_request'),

    path('<int:event_id>/participants/<int:participant_id>/update/', participant_update, name='participant_update'),
    path('<int:event_id>/participants/<int:participant_id>/delete/', participant_delete, name='participant_delete'),
    path('<int:event_id>/qr_code/', generate_qr_code, name='generate_qr_code'),
    path('<int:event_id>/event_statistique/', event_statistique, name='event_statistique'),

    # URL for sending email related to participants of the event
    path('<int:event_id>/participants/send-email/', send_email, name='send_email'),  # Updated to use send_email
    

    path('<int:event_id>/participants/generate-image/', generate_image, name='generate_image'),


    path('<int:event_id>/participants/text-to-speech/', text_to_speech, name='text_to_speech'),


    path('<int:event_id>/participants/chat/', chat_with_api, name='chat_with_api'),


    path('<int:event_id>/participants/face_analyzer/', analyze_face, name='analyze_face'),

]