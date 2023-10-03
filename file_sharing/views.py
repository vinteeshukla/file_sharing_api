from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import FileUpload, DownloadToken
from .serializers import FileUploadSerializer
from django.shortcuts import get_object_or_404
from .serializers import *

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

@api_view(['POST'])
def register_user(request):
    """
    User registration view. Creates a new user.
    """
    if request.method == 'POST':
        # Extract user registration data from the request
        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email')

        # Check if the username or email is already in use
        if User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists():
            return Response({'message': 'Username or email already in use.'}, status=status.HTTP_400_BAD_REQUEST)

        # Create a new user with a hashed password
        user = User.objects.create_user(username=username, password=password, email=email)

        # You can also optionally send an email verification here

        return Response({'message': 'User registered successfully.'}, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def register_user1(request):
    """
    User registration view. Creates a new user.
    """
    if request.method == 'POST':
        # Assuming you have a User model and UserSerializer
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User registered successfully.'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login(request):
    """
    User login view. Authenticates the user and returns an access token.
    """
    if request.method == 'POST':
        # Extract user login credentials from the request
        username = request.data.get('username')
        password = request.data.get('password')

        # Authenticate the user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Authentication successful, log the user in
            login(request, user)
            return Response({'message': 'Login successful.'}, status=status.HTTP_200_OK)
        else:
            # Authentication failed, display an error message
            return Response({'message': 'Login failed. Invalid credentials.'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
def login1(request):
    """
    User login view. Authenticates the user and returns an access token.
    """
    if request.method == 'POST':
        # Implement user authentication logic here
        # For a basic example, you can check if the provided credentials are correct
        username = request.data.get('username')
        password = request.data.get('password')

        if username == 'your_username' and password == 'your_password':
            return Response({'message': 'Login successful.'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Login failed. Invalid credentials.'}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
def upload_file(request):
    """
    File upload view. Allows users to upload files.
    """
    if request.method == 'POST':
        # Check if the uploaded file type is allowed (e.g., pptx, docx, xlsx)
        allowed_file_types = ['pptx', 'docx', 'xlsx']
        file = request.FILES.get('file')
        
        if not file:
            return Response({'message': 'File not provided.'}, status=status.HTTP_400_BAD_REQUEST)
        
        file_extension = file.name.split('.')[-1].lower()
        if file_extension not in allowed_file_types:
            return Response({'message': 'File type not allowed.'}, status=status.HTTP_400_BAD_REQUEST)

        # Save the uploaded file
        file_upload = FileUpload(file=file)
        file_upload.save()
        return Response({'message': 'File uploaded successfully.'}, status=status.HTTP_201_CREATED)

@api_view(['GET'])
def list_uploaded_files(request):
    """
    List all uploaded files view. Lists all uploaded files.
    """
    if request.method == 'GET':
        uploaded_files = FileUpload.objects.all()
        serializer = FileUploadSerializer(uploaded_files, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def download_file(request, file_id):
    if request.method == 'GET':
        file_upload = get_object_or_404(FileUpload, pk=file_id)
        
        download_url = f"/download-file/{file_upload.id}/"

        return Response({'download-link': download_url, 'message': 'success'}, status=status.HTTP_200_OK)

