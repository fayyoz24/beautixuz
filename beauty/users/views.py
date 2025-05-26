from rest_framework import generics, status
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .serializers import SignupSerializer
import random
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate
from rest_framework import generics, status
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .serializers import SignupSerializer
import random
from rest_framework import serializers

User = get_user_model()

confirmation_codes = {}  # Temporary for demo; use DB/Redis in production

class SignupView(generics.CreateAPIView):
    serializer_class = SignupSerializer

    def perform_create(self, serializer):
        user = serializer.save()
        code = random.randint(1000, 9999)
        confirmation_codes[user.phone_number] = str(code)
        print(f"[DEBUG] Confirmation code for {user.phone_number}: {code}")


class ConfirmPhoneView(APIView):
    def post(self, request):
        phone = request.data.get('phone_number')
        code = request.data.get('code')
        if confirmation_codes.get(phone) == code:
            user = User.objects.get(phone_number=phone)
            user.phone_confirmed = True
            user.save()
            return Response({'detail': 'Phone confirmed'})
        return Response({'detail': 'Invalid code'}, status=400)


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        # Add extra responses
        data.update({
            'username': self.user.username,
            # Add any custom fields as needed
            'user_type': getattr(self.user, 'user_type', None),  # If you have a custom field
        })

        return data


class LoginView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer