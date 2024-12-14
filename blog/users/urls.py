from django.urls import path
from .views import *
from django.conf.urls.static import static
from django.urls import path
from django.conf import settings

urlpatterns = [
    # CoachNutri URLs
    path('create-coach-nutri/', add_CoachNutri, name='create_coach_nutri'),
    path('delete-coach-nutri/<int:CoachNutriId>/', delete_CoachNutri, name='delete_coach_nutri'),
    path('update-coach-nutri/<int:CoachNutriId>/', update_CoachNutri, name='update_coach_nutri'),
    path('all-coach-nutri/', view_CoachNutri, name='view_coach_nutri'),
    path('stats/', statistics_view, name='stats'),
    path('request-password-reset/', request_password_reset, name='request_password_reset'),
    path('reset-password/', reset_password, name='reset_password'),
    path('coach-face-login/', coach_face_login, name='coach_face_login'),
    
    
    # Coach-related URLs
    path('profile-coach/', get_user_profile, name='coach_profile'),
    path('<int:coach_id>/clients/', get_coach_clients, name='get_coach_clients'),
    
    # Program Assignment URLs
    path('assign-program/<int:client_id>/', assign_program, name='assign_program'),
    path('delete-program/<int:client_id>/', delete_program, name='delete_program'),

    # Client URLs
    path('create-client/', add_Client, name='create_client'),
    path('delete-client/<int:ClientId>/', delete_Client, name='delete_client'),
    path('update-client/<int:ClientId>/', update_Client, name='update_client'),
    path('all-client/', view_Client, name='view_client'),
    path('profile-client/', get_client_profile, name='client_profile'),
    path('update-profile-client/', update_client_profile, name='update_client_profile'),
     path('get_program/<str:program_type>/', get_program_data, name='get_program'),
    path('profile-client/program_fitness/', 
         program_client_view, 
         {'program_type': 'fitness'}, 
         name='program_fitness'),
    path('profile-client/program_nutrition/', 
         program_client_view, 
         {'program_type': 'nutrition'}, 
         name='program_nutrition'),
    
    # Authentication URLs
    path('login-coach/', login, name='coach_login'),
    path('logout-coach/', logout_view, name='coach_logout'),
    path('login-client/', login, name='client_login'),
    path('logout-client/', logout_view, name='client_logout'),
    path('register-client/', register_client, name='client_register'),
    
    
    
    path('class-timetable/',program,name="class-timetable"),

]
