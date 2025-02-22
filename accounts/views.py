from django.contrib.auth import authenticate, get_user_model
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegisterSerializer, UserSerializer, TokenSerializer

User = get_user_model()

class RegisterAPIView(APIView):
    """New user registration"""

    @swagger_auto_schema(
        request_body=RegisterSerializer,
        responses={201: UserSerializer, 400: "Validation Error"}
    )
    def post(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(UserSerializer(user).data,
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(APIView):
    """User authorisation and receipt of JWT tokens"""

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['email', 'password'],
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING,
                                        format=openapi.FORMAT_EMAIL),
                'password': openapi.Schema(type=openapi.TYPE_STRING,
                                           format=openapi.FORMAT_PASSWORD)
            }
        ),
        responses={
            200: TokenSerializer,
            400: openapi.Response(description="Missing email or password"),
            401: openapi.Response(description="Incorrect credentials")
        }
    )
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return Response({'detail': 'Email and password must be specified'},
                            status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(email=email, password=password)

        if not user:
            return Response({'detail': 'Incorrect credentials'},
                            status=status.HTTP_401_UNAUTHORIZED)

        refresh = RefreshToken.for_user(user)

        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh)
        }, status=status.HTTP_200_OK)


class UserProfileAPIView(APIView):
    """Retrieving and updating a user profile"""
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        responses={
            200: UserSerializer,
            401: "Unauthorized"
        }
    )
    def get(self, request, *args, **kwargs):
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=UserSerializer,
        responses={
            200: UserSerializer,
            400: "Validation Error",
            401: "Unauthorized"
        }
    )
    def put(self, request, *args, **kwargs):
        serializer = UserSerializer(request.user,
                                    data=request.data,
                                    partial=True)  # Разрешает обновлять только переданные поля
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
