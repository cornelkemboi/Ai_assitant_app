# api/views.py

# Import necessary modules and classes
import spacy
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import generics, status, permissions
from rest_framework.authentication import BaseAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Document
from .serializers import UserSerializer, DocumentSerializer

# Load the spaCy language model
nlp = spacy.load('en_core_web_sm')


class CustomAuthToken(ObtainAuthToken):
    """
    Custom authentication token view that handles user authentication and token generation.
    Extends ObtainAuthToken to provide a custom response format.
    """
    def post(self, request, *args, **kwargs):
        # Validate incoming request data
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        # Generate or retrieve the authentication token for the user
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })


class CustomTokenAuthentication(BaseAuthentication):
    """
    Custom token authentication class that retrieves the user based on the provided token.
    """
    def authenticate(self, request):
        # Extract the token from the Authorization header
        token = request.META.get('HTTP_AUTHORIZATION', '').split(' ')[-1]
        try:
            # Retrieve the user associated with the token
            user = User.objects.get(auth_token=token)
            return (user, token)
        except User.DoesNotExist:
            raise AuthenticationFailed('Invalid token')


class RegisterView(generics.CreateAPIView):
    """
    View to handle user registration.
    Allows any user to create a new account.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]


class LoginView(APIView):
    """
    View to handle user login and JWT token generation.
    Authenticates the user and returns a JWT token if credentials are valid.
    """
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)

        if user is not None:
            # Generate JWT tokens for the authenticated user
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        else:
            return Response({'detail': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)


class DocumentUploadView(generics.CreateAPIView):
    """
    View to handle document upload.
    Requires authentication and uses custom token authentication.
    On successful upload, improves the document content using spaCy.
    """
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    authentication_classes = [CustomTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)
        document = serializer.instance
        # Read the content of the uploaded file
        with open(document.original_file.path, 'rb') as file:
            try:
                content = file.read().decode('utf-8')
            except UnicodeDecodeError:
                content = file.read().decode('latin-1')
        # Improve the document content
        improved_content = improve_document(content)

        document.improved_content = improved_content
        document.save()
        return Response({'success': 'File uploaded successfully'}, status=status.HTTP_201_CREATED)


def improve_document(content):
    """
    Improve the document content using spaCy NLP.
    Adds '[Improved]' to each sentence in the document.
    """
    doc = nlp(content)
    suggestions = []
    for sent in doc.sents:
        suggestions.append(sent.text + " [Improved]")
    return ' '.join(suggestions)


class DocumentDetailView(generics.RetrieveAPIView):
    """
    View to retrieve the details of a specific document.
    Only accessible to the authenticated user who owns the document.
    """
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Filter documents to include only those owned by the authenticated user
        return self.queryset.filter(user=self.request.user)
