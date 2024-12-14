from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, BasePermission
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from django.contrib.auth import get_user_model, authenticate
from .models import Client, CoachNutritionist
from .serializers import *
from django.conf import settings
from django.shortcuts import get_list_or_404,get_object_or_404
from pathlib import Path
import csv
import os
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.db.models import Avg, Count
from django.http import JsonResponse
from django.shortcuts import render
from django.core.mail import send_mail
from django.utils import timezone
from .models import PasswordResetToken
import numpy as np
import requests
import face_recognition
import io
from PIL import Image
from django.core.validators import URLValidator
from django.views.decorators.csrf import csrf_exempt

def program(request):
    return render(request, 'class-timetable.html')
def home(request):
    return render(request, 'index.html')
class IsSuperUser(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_superuser

def load_image_from_url(url):
    """
    Load an image from a URL using requests and PIL.
    
    Args:
        url (str): URL of the image
    
    Returns:
        numpy.ndarray: Image as a numpy array
    """
    try:
        # Validate URL
        URLValidator()(url)
        
        # Download image
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        # Open image from bytes
        image = Image.open(io.BytesIO(response.content))
        
        # Convert to RGB (in case of RGBA or other formats)
        image = image.convert('RGB')
        
        # Convert to numpy array
        return np.array(image)
    except Exception as e:
        print(f"Error loading image from {url}: {e}")
        return None

def encode_coach_faces():
    """Encode faces for all coaches using online profile pictures."""
    known_face_encodings = []
    known_coach_ids = []

    coaches = CoachNutritionist.objects.all()
    for coach in coaches:
        # Use the profile picture URL
        image_url = coach.photo

        try:
            # Load image from URL
            coach_image = load_image_from_url(image_url)
            
            if coach_image is not None:
                # Detect face encodings
                face_encodings = face_recognition.face_encodings(coach_image)
                
                if face_encodings:
                    known_face_encodings.append(face_encodings[0])
                    known_coach_ids.append(coach.id)
        except Exception as e:
            print(f"Error processing coach {coach.id} image: {e}")

    return known_face_encodings, known_coach_ids
@csrf_exempt 
@api_view(['POST'])
def coach_face_login(request):
    """Face recognition login for coaches using uploaded image."""
    if 'image' not in request.FILES:
        return Response({"error": "No image uploaded"}, status=status.HTTP_400_BAD_REQUEST)

    # Read uploaded image file
    uploaded_image = request.FILES['image']
    uploaded_image_array = face_recognition.load_image_file(uploaded_image)
    
    # Detect face encodings in uploaded image
    uploaded_face_encodings = face_recognition.face_encodings(uploaded_image_array)
    
    if not uploaded_face_encodings:
        return Response({"error": "No face detected in uploaded image"}, status=status.HTTP_404_NOT_FOUND)

    # Get known coach faces
    known_face_encodings, known_coach_ids = encode_coach_faces()

    if not known_face_encodings:
        return Response({"error": "No coach faces available for comparison"}, status=status.HTTP_404_NOT_FOUND)

    # Compare faces
    for uploaded_face_encoding in uploaded_face_encodings:
        # Compute face distances
        face_distances = face_recognition.face_distance(known_face_encodings, uploaded_face_encoding)
        best_match_index = np.argmin(face_distances)
        
        # Face match threshold
        if face_distances[best_match_index] < 0.6:
            # Find matching coach
            coach_id = known_coach_ids[best_match_index]
            coach = CoachNutritionist.objects.get(id=coach_id)
            
            # Generate tokens
            refresh = RefreshToken.for_user(coach)
            
            return Response({
                'user': {
                    'id': coach.id,
                    'username': coach.username,
                    'email': coach.email,
                    'is_coach': True,
                },
                'token': {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }
            }, status=status.HTTP_200_OK)

    # No match found
    return Response({"error": "Face not recognized"}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
def request_password_reset(request):
    """Allow coaches or nutritionists to request a password reset for a client."""
    
    print(request.data)
    serializer = PasswordResetRequestSerializer(data=request.data)
    
    if serializer.is_valid():
        identifier = serializer.validated_data['identifier']
        print(f"Received identifier: {identifier}")
        
        # Attempt to find the user by identifier (email or username)
        try:
            # Try fetching the user by email
            user = get_user_model().objects.get(email=identifier)
        except get_user_model().DoesNotExist:
            # If not found by email, try fetching by username (if it's allowed to use a username)
            try:
                user = get_user_model().objects.get(username=identifier)
            except get_user_model().DoesNotExist:
                return Response({"error": "User does not exist."}, status=status.HTTP_404_NOT_FOUND)

        # Create a password reset token
        token = PasswordResetToken.objects.create(
            user=user,
            expires_at=timezone.now() + timezone.timedelta(hours=1)  # Token valid for 1 hour
        )
        
        # Generate the reset link using the token
        reset_link = f"http://127.0.0.1:3000/users/reset-password/{token.token}/"  # React app running on port 3000

        # Email content
        subject = "Password Reset Request"
        message = f"Hello {user.first_name},\n\n" \
                  f"You requested a password reset for your account. To reset your password, " \
                  f"click the link below:\n\n{reset_link}\n\n" \
                  f"If you did not request a password reset, please ignore this email.\n\n" \
                  f"Best regards,\nYour Support Team"
        
        print("Before sending email")
        # Send email with the password reset link
        try:
            send_mail(
                subject,
                message,
                'no-reply@yourdomain.com',  # Sender email
                [identifier],  # Recipient (email)
                fail_silently=False,
            )
            print("Email sent successfully")
        except Exception as e:
            print(f"Error sending email: {e}")
            return Response({"error": "Failed to send email."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({"message": "Password reset link has been sent to the user's email."}, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def reset_password(request):
    """Handle password reset confirmations."""
    serializer = PasswordResetConfirmSerializer(data=request.data)
    if serializer.is_valid():
        token_value = serializer.validated_data['token']
        new_password = serializer.validated_data['new_password']

        try:
            token = PasswordResetToken.objects.get(token=token_value)
            if token.is_expired():
                return Response({"error": "Token has expired."}, status=status.HTTP_400_BAD_REQUEST)

            user = token.user
            user.set_password(new_password)
            user.save()

            # Delete the token after it is used
            token.delete()

            return Response({"message": "Password has been reset successfully."}, status=status.HTTP_200_OK)
        except PasswordResetToken.DoesNotExist:
            return Response({"error": "Invalid token."}, status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@permission_classes([IsAuthenticated])
@api_view(['GET'])
def statistics_view(request):
    # Statistiques des clients
    user = request.user

    if not (user.is_coach or user.is_nutritionist):
        return Response({"error": "User is not authorized to access this data"}, status=403)

    try:
        coach_nutritionist = CoachNutritionist.objects.get(pk=user.pk)
    except CoachNutritionist.DoesNotExist:
        return Response({"error": "No associated Coach/Nutritionist found for the user"}, status=404)

    clients = coach_nutritionist.client_id.all()

    total_clients = clients.count()
    avg_age = clients.aggregate(Avg('age'))['age__avg'] or 'N/A'
    avg_weight = clients.aggregate(Avg('weight'))['weight__avg'] or 'N/A'
    avg_height = clients.aggregate(Avg('height'))['height__avg'] or 'N/A'
    avg_goal_weight = clients.aggregate(Avg('goal_weight'))['goal_weight__avg'] or 'N/A'

    program_fitness_count = clients.filter(program_fitness__isnull=False).exclude(program_fitness="").distinct().count()
    program_nutrition_count = clients.filter(program_nutrition__isnull=False).exclude(program_nutrition="").distinct().count()

    # Comptage des sexes
    male_count = clients.filter(sexe='Homme').count()
    female_count = clients.filter(sexe='Femme').count()

    data = {
        'total_clients': total_clients,
        'avg_age': avg_age,
        'avg_weight': avg_weight,
        'avg_height': avg_height,
        'avg_goal_weight': avg_goal_weight,
        'program_fitness_count': program_fitness_count,
        'program_nutrition_count': program_nutrition_count,
        'male_count': male_count,
        'female_count': female_count
    }

    return Response(data)

@api_view(['GET'])
def get_coach_clients(request, coach_id):
    try:
        # Récupérer le coach par ID
        coach = CoachNutritionist.objects.get(id=coach_id)
        
        # Récupérer tous les clients associés à ce coach
        clients = coach.client_id.all()  # Assurez-vous que `client_id` est bien une relation ManyToMany vers `Client`
        
        # Sérialiser les clients
        serializer = ClientSerializer(clients, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
    
    except CoachNutritionist.DoesNotExist:
        return Response({'error': 'Coach not found.'}, status=status.HTTP_404_NOT_FOUND)@permission_classes([IsAuthenticated])
    
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_program(request, client_id):
    # Get the client by ID
    client = get_object_or_404(Client, id=client_id)

    # Clear the program fields (assuming these are file fields)
    if client.program_fitness or client.program_nutrition:
        client.program_fitness.delete(save=False)
        client.program_nutrition.delete(save=False)
        client.save()

        return Response(
            {"message": "Program deleted successfully."},
            status=status.HTTP_204_NO_CONTENT
        )

    # If no program was associated with the client
    return Response(
        {"error": "No program found for this client."},
        status=status.HTTP_404_NOT_FOUND
    )    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_profile(request):
    user = request.user
    # Ensure the user is authenticated
    if not user.is_authenticated:
        return Response({"detail": "Authentication credentials were not provided."}, status=401)
    
    # Prepare user profile data
    user_profile = {
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'is_active': user.is_active,
        'is_staff': user.is_staff,
        'is_superuser': user.is_superuser,
        'is_client': getattr(user, 'is_client', False),
        'is_coach': getattr(user, 'is_coach', False),
        'is_nutritionist': getattr(user, 'is_nutritionist', False),
    }

    # Check if the user is a CoachNutritionist and retrieve the instance
    if user.is_coach or user.is_nutritionist:
        try:
            coach_nutritionist_instance = CoachNutritionist.objects.get(pk=user.pk)
            user_profile.update({
                'certifications': coach_nutritionist_instance.certifications or '',
                'bio': coach_nutritionist_instance.bio or '',
                'photo': coach_nutritionist_instance.photo,
            })
        except CoachNutritionist.DoesNotExist:
            user_profile.update({
                'certifications': '',
                'bio': '',
                'photo': None,
            })
    else:
        user_profile.update({
            'certifications': '',
            'bio': '',
            'photo': None,
        })

    return Response(user_profile)

@permission_classes([IsAuthenticated])
@api_view(['GET'])
def get_client_profile(request):
    user = request.user

    # Prepare user profile data
    user_profile = {
        'userId': user.id,
        'username': user.username,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email,
        'is_active': user.is_active,
        'is_staff': user.is_staff,
        'is_superuser': user.is_superuser,
        'is_client': getattr(user, 'is_client', False),
        'is_coach': getattr(user, 'is_coach', False),
        'is_nutritionist': getattr(user, 'is_nutritionist', False),
    }

    # Check if the user is a Client
    if user.is_client:
        try:
            client_instance = Client.objects.get(pk=user.pk)
            user_profile.update({
                'age': client_instance.age,
                'weight': client_instance.weight,
                'height': client_instance.height,
                'goal_weight': client_instance.goal_weight,
                'activity_level': client_instance.activity_level,
                'profile_picture': client_instance.profile_picture,
                'sexe': client_instance.sexe,
                'program_fitness': os.path.join(settings.MEDIA_ROOT, client_instance.program_fitness.name) if client_instance.program_fitness else None,
                'program_nutrition': os.path.join(settings.MEDIA_ROOT, client_instance.program_nutrition.name) if client_instance.program_nutrition else None,
            })
        except Client.DoesNotExist:
            user_profile.update({
                'age': None,
                'weight': None,
                'height': None,
                'goal_weight': None,
                'activity_level': None,
                'profile_picture': None,
                'program_nutrition': None,
                'program_fitness': None,
            })

    return Response(user_profile)


def get_client_programs(request, client_id):
    # Get the Client object by client_id
    client = get_object_or_404(Client, id=client_id)
    
    # Retrieve the file URLs for the nutrition and fitness programs
    program_data = {
        'program_fitness': {
            'name': client.program_fitness.name if client.program_fitness else None,
            'file_url': client.program_fitness.url if client.program_fitness else None
        },
        'program_nutrition': {
            'name': client.program_nutrition.name if client.program_nutrition else None,
            'file_url': client.program_nutrition.url if client.program_nutrition else None
        }
    }

    # Return a JSON response with the program data
    return JsonResponse(program_data)
# Inscription d'un client
@api_view(['POST'])
def register_client(request):
    print(request.data)
    serializer = ClientSerializer(data=request.data)
    if serializer.is_valid():
        client = serializer.save(is_client=True)
        return Response(ClientSerializer(client).data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Login
@api_view(['POST'])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')

    if not username or not password:
        return Response({'error': 'Username and password are required.'}, status=status.HTTP_400_BAD_REQUEST)

    user = authenticate(username=username, password=password)

    if user is None:
        return Response({'error': 'Invalid credentials.'}, status=status.HTTP_401_UNAUTHORIZED)

    if not user.is_active:
        return Response({'error': 'User account is inactive.'}, status=status.HTTP_403_FORBIDDEN)

    # Generate tokens
    refresh = RefreshToken.for_user(user)
    access_token = refresh.access_token

    # Check if the user is a superuser and return basic user info if true
    if user.is_superuser:
        user_data = {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "is_superuser": user.is_superuser
        }
    elif user.is_client:
        client_instance = Client.objects.get(pk=user.pk)
        serializer = ClientSerializer(client_instance)
        user_data = serializer.data
    else:
        coach_nutritionist_instance = CoachNutritionist.objects.get(pk=user.pk)
        serializer = CoachNutriSerializer(coach_nutritionist_instance)
        user_data = serializer.data

    return Response({
        'user': user_data,
        'token': {
            'refresh': str(refresh),
            'access': str(access_token),
        }
    }, status=status.HTTP_200_OK)
# Logout
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    try:
        # Get the refresh token from the request data
        refresh_token = request.data.get("refresh")
        if refresh_token:
            # Create a RefreshToken instance to handle invalidation
            token = RefreshToken(refresh_token)
            # Blacklist the refresh token
            token.blacklist()
            return Response({"detail": "Logout successful."}, status=status.HTTP_205_RESET_CONTENT)
        else:
            return Response({"detail": "No refresh token provided."}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
# Gestion des Coach/Nutritionist
@api_view(['GET'])
@permission_classes([IsAuthenticated, IsSuperUser])
def view_CoachNutri(request):
    items = CoachNutritionist.objects.filter(**request.query_params.dict()) if request.query_params else CoachNutritionist.objects.all()
    if items:
        serializer = CoachNutriSerializer(items, many=True)
        return Response(serializer.data)
    return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
@permission_classes([IsAuthenticated, IsSuperUser])
def add_CoachNutri(request):
    serializer = CoachNutriSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()  # This will call the `create` method in the serializer
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated, IsSuperUser])
def delete_CoachNutri(request, CoachNutriId):
    try:
        coach_nutri = CoachNutritionist.objects.get(id=CoachNutriId)
        coach_nutri.delete()
        return Response({'message': 'Coach/Nutritionist deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
    except CoachNutritionist.DoesNotExist:
        return Response({'error': 'Coach/Nutritionist not found.'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['PUT'])
@permission_classes([IsAuthenticated, IsSuperUser])
def update_CoachNutri(request, CoachNutriId):
    try:
        coach_nutri = CoachNutritionist.objects.get(id=CoachNutriId)
        
        # Extract client IDs from request data and update the ManyToMany field
        client_ids = request.data.get('client_id', [])
        if client_ids:
            # Fetch Client instances based on provided IDs
            clients = Client.objects.filter(id__in=client_ids)
            if clients.count() != len(client_ids):
                return Response({'error': 'One or more client IDs are invalid.'}, status=status.HTTP_400_BAD_REQUEST)
            # Update the clients associated with the coach/nutritionist
            coach_nutri.client_id.set(clients)  # Use .set() to replace current relations
        
        # Save other fields if provided
        serializer = CoachNutriSerializer(coach_nutri, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    except CoachNutritionist.DoesNotExist:
        return Response({'error': 'Coach/Nutritionist not found.'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def assign_program(request,client_id):
    try:
        client = Client.objects.get(id=client_id)
    except Client.DoesNotExist:
        return Response({"detail": "Client not found"}, status=status.HTTP_404_NOT_FOUND)

    # Check if the file is in the request
    if 'file' not in request.FILES:
        return Response({"detail": "No file provided"}, status=status.HTTP_400_BAD_REQUEST)

    uploaded_file = request.FILES['file']
    
    # Example of saving the file
    # Saving it to the default storage (e.g., MEDIA_ROOT)
    file_name = uploaded_file.name
    file_path = default_storage.save(f'programs/{file_name}', ContentFile(uploaded_file.read()))

    # Optionally, associate the file path with the client model
    client.program_fitness = file_path  # Assuming you have a field for this
    client.save()

    return Response({"detail": "File uploaded successfully"}, status=status.HTTP_200_OK)


# Gestion des Clients
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def view_Client(request):
    items = Client.objects.filter(**request.query_params.dict()) if request.query_params else Client.objects.all()
    if items:
        serializer = ClientSerializer(items, many=True)
        return Response(serializer.data)
    return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_Client(request):
    serializer = ClientSerializer(data=request.data)
    if serializer.is_valid():
        client = serializer.save(is_client=True)
        return Response(ClientSerializer(client).data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_Client(request, ClientId):
    try:
        client = Client.objects.get(id=ClientId)
        client.delete()
        return Response({'message': 'Client deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
    except Client.DoesNotExist:
        return Response({'error': 'Client not found.'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_Client(request, ClientId):
    try:
        client = Client.objects.get(id=ClientId)
        serializer = ClientSerializer(client, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
    except Client.DoesNotExist:
        return Response({'error': 'Client not found.'}, status=status.HTTP_404_NOT_FOUND)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_client_profile(request):
    print(request.data)
    try:
        client = Client.objects.get(pk=request.user.pk)  # Assuming `id` is tied to the logged-in user
    except Client.DoesNotExist:
        return Response({"error": "Client not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = ClientSerializer(client, data=request.data, partial=True)  # Allow partial updates
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def read_fitness_csv():
    """Read and parse the fitness program CSV file."""
    fitness_data = []
    current_day_data = None
    
    csv_path = Path(settings.BASE_DIR) / 'data' / 'fitness_program.csv'
    
    with open(csv_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')
        for row in reader:
            if row['Day']:  # New day entry
                if current_day_data:
                    fitness_data.append(current_day_data)
                current_day_data = {
                    'day': row['Day'],
                    'type': row['Type of Program'],
                    'exercises': []
                }
            
            if row['Exercises']:  # Add exercise to current day
                current_day_data['exercises'].append({
                    'name': row['Exercises'],
                    'sets_reps': row['Sets/Reps']
                })
                
        # Add the last day's data
        if current_day_data:
            fitness_data.append(current_day_data)
            
    return fitness_data

def read_nutrition_csv():
    """Read and parse the nutrition program CSV file."""
    nutrition_data = []
    current_day_data = None
    
    csv_path = Path(settings.BASE_DIR) / 'data' / 'nutrition_program.csv'
    
    with open(csv_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')
        for row in reader:
            if row['Day']:  # New day entry
                if current_day_data:
                    nutrition_data.append(current_day_data)
                current_day_data = {
                    'day': row['Day'],
                    'meals': []
                }
            
            if row['Meal']:  # Add meal to current day
                current_day_data['meals'].append({
                    'time': row['Meal Times'],
                    'meal': row['Meal'],
                    'quantity': row['Quantity']
                })
                
        # Add the last day's data
        if current_day_data:
            nutrition_data.append(current_day_data)
            
    return nutrition_data

def program_client_view(request, program_type=None):
    """
    View function to display either fitness or nutrition program based on URL.
    """
    context = {
        'show_fitness': True,
        'show_nutrition': True
    }
    
    try:
        if program_type == 'fitness':
            context['fitness_program'] = read_fitness_csv()
            context['show_nutrition'] = False
        elif program_type == 'nutrition':
            context['nutrition_program'] = read_nutrition_csv()
            context['show_fitness'] = False
        else:
            # Load both programs for the main view
            context['fitness_program'] = read_fitness_csv()
            context['nutrition_program'] = read_nutrition_csv()
            
    except FileNotFoundError:
        context['error'] = 'Program data files not found'
    except Exception as e:
        context['error'] = f'Error loading program data: {str(e)}'
    
    return render(request, 'profile-client/program.html', context)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_program_data(request, program_type):
    import csv
    import io
    from django.http import JsonResponse

    # Get the current logged-in client
    client = request.user.client

    # Helper function to process a program file
    def process_program(file, program_type):
        if not file:
            return None, {'error': f'No {program_type} program available'}

        # Read CSV file
        decoded_file = file.read().decode('utf-8').strip()
        csv_data = list(csv.reader(io.StringIO(decoded_file), delimiter=';'))

        # Skip the first line (header)
        csv_data = csv_data[1:]

        # Verify data integrity
        if not csv_data:
            return None, {'error': f'Empty {program_type} program file'}

        # Fill empty day and type values and process data
        filled_data = {}
        last_day = ''
        last_type = ''
        current_entry = None

        for row in csv_data:
            day = row[0] if row[0].strip() else last_day
            type_prog = row[1] if row[1].strip() else last_type

            last_day = day
            last_type = type_prog

            if program_type == 'fitness':
                if day not in filled_data or not current_entry or current_entry['day'] != day:
                    if current_entry:
                        filled_data[current_entry['day']] = current_entry
                    current_entry = {
                        'day': day,
                        'type': type_prog,
                        'exercises': [row[2]],
                        'sets_reps': [row[3]]
                    }
                else:
                    current_entry['exercises'].append(row[2])
                    current_entry['sets_reps'].append(row[3])
            else:
                if day not in filled_data:
                    filled_data[day] = {
                        'day': day,
                        'meal_times': [],
                        'meals': [],
                        'quantities': []
                    }
                filled_data[day]['meal_times'].append(row[1])
                filled_data[day]['meals'].append(row[2])
                filled_data[day]['quantities'].append(row[3])

        if program_type == 'fitness' and current_entry:
            filled_data[current_entry['day']] = current_entry

        return list(filled_data.values()), None

    # Handle "all" case
    if program_type == 'all':
        fitness_data, fitness_error = process_program(client.program_fitness, 'fitness')
        nutrition_data, nutrition_error = process_program(client.program_nutrition, 'nutrition')

        # Collect errors if both programs are unavailable
        if fitness_error and nutrition_error:
            return JsonResponse({'errors': [fitness_error, nutrition_error]}, status=404)

        response_data = {
            'fitness': fitness_data if not fitness_error else fitness_error,
            'nutrition': nutrition_data if not nutrition_error else nutrition_error,
        }
        return JsonResponse(response_data)

    # Handle individual program types
    elif program_type in ['fitness', 'nutrition']:
        program_file = client.program_fitness if program_type == 'fitness' else client.program_nutrition
        program_data, program_error = process_program(program_file, program_type)

        if program_error:
            return JsonResponse(program_error, status=404)

        return JsonResponse(program_data, safe=False)

    return JsonResponse({'error': 'Invalid program type'}, status=400)
