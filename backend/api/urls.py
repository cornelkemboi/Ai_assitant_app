# api/urls.py
from django.urls import path
from .views import RegisterView, CustomAuthToken, DocumentUploadView, DocumentDetailView
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt.views import TokenVerifyView

urlpatterns = [
    path('api/token-auth/', obtain_auth_token, name='api_token_auth'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('register/', RegisterView.as_view(), name='register'),
    # path('login/', CustomAuthToken.as_view(), name='login'),
    path('login/', CustomAuthToken.as_view(), name='login'),
    path('upload/', DocumentUploadView.as_view(), name='upload'),
    path('documents/<int:pk>/', DocumentDetailView.as_view(), name='document_detail'),
]
