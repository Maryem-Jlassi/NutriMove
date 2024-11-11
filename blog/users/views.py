from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, BasePermission
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from django.contrib.auth import get_user_model, authenticate
from .models import Client, CoachNutritionist
from .serializers import ClientSerializer, CoachNutriSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.shortcuts import get_list_or_404,get_object_or_404
import os
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
class IsSuperUser(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_superuser

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
            # Retrieve the Client instance using the user instance
            client_instance = Client.objects.get(pk=user.pk)
            user_profile.update({
                'age': client_instance.age,
                'weight': client_instance.weight,
                'height': client_instance.height,
                'goal_weight': client_instance.goal_weight,
                'activity_level': client_instance.activity_level,
                'profile_picture': client_instance.profile_picture,
                'program_nutrition': client_instance.program_nutrition.url,
                'program_fitness': client_instance.program_fitness.url ,
            })
        except Client.DoesNotExist:
            # Handle the case where the user is not found in the Client table
            user_profile.update({
                'age': None,
                'weight': None,
                'height': None,
                'goal_weight': None,
                'activity_level': None,
                'profile_picture': None,
                'program_nutrition': '',
                'program_fitness': '',
            })
    return Response(user_profile)

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

    # Check user role based on URL and user type
    #if 'login-client' in request.path and not (user.is_client or user.is_superuser):
        #return Response({'error': 'Only clients or superusers can access this login.'}, status=status.HTTP_403_FORBIDDEN)
    #elif 'login-coach' in request.path and not (user.is_coach or user.is_nutritionist or user.is_superuser):
        #return Response({'error': 'Only coaches, nutritionists, or superusers can access this login.'}, status=status.HTTP_403_FORBIDDEN)

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
