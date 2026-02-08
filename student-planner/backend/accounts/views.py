from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView 
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from datetime import *
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from django.core.validators import validate_email
from django.core.exceptions import ValidationError


from .serializers import UserSerializer, OTPVerifySerailizer
from .models import UserProfile
from .utils import generate_otp, send_otp_email, is_otp_valid

# Create your views here.
@method_decorator(csrf_exempt, name='dispatch')
class RegisterView(generics.CreateAPIView):
    
    """POST /api/register/
      Register a new user"""
    queryset = User.objects.all()
    serializer_class = UserSerializer

# email validation
    def create(self, request, *args, **kwargs):
        email=request.data.get('email')
        if email:
            try:
                validate_email(email)
            except ValidationError:
                return Response(
                    {'error':'Invalid email format'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        return super().create(request, *args, **kwargs)
    

@method_decorator(csrf_exempt, name='dispatch')
class LoginStep1View(APIView):
    """
    Docstring for LoginStep1View
    POST /api/login-step1/
    Step 1:Verify username/password and send OTP

    Request body:{
        "username":"string",
        "password":"password123"
    }

    Response:{
        "status": "otp_sent",
        "message": "OTP has been sent to your registered email.",
        "username":"testuser"
    }
    """

    def post(self,request):
        username=request.data.get('username')
        password=request.data.get('password')

        if not username or not password:
            return Response(
                {'error': 'Username and password required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        user = authenticate(username=username, password=password)

        if not user:
            return Response(
                {'error': 'Invalid credentials'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        if not user.email:
            return Response(
                {'error':'User does not have an email. Contact support.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        # get or create user profile
        profile, created=UserProfile.objects.get_or_create(user=user)

        # generate OTP
        otp_code=generate_otp()
        print(f"Generated OTP for {username}: {otp_code}")

        # save OTP and timestamp to database
        profile.otp_code = otp_code
        profile.otp_created_at = timezone.now()
        profile.save()

        # send OTP to user's email
        email_sent=send_otp_email(user.email, otp_code)

        if not email_sent:
            profile.otp_code=None
            profile.otp_created_at=None
            profile.save()

            return Response(
                {
                    'error': 'Failed to send OTP. Please check your email address and try again',
                    'email':user.email
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            ),
        
        return Response({
            'status':'otp_sent',
            'message':f'OTP sent to {user.email}',
            'username':username,
            'email':user.email
        })

@method_decorator(csrf_exempt, name='dispatch')
class LoginStep2View(APIView):
        """
        POST /api/auth/login/step2
        Step 2: Verify OTP and issue JWT tokens

        Request body:
        {
            "username":"testuser",
            "otp":"123456"
        }

        Response:
        {
            "access":"jwt_access_token",
            "refresh":"jwt_refresh_token",
            "username":"testuser",
            "email":"user@example.com"
        }
        """

        def post(self, request):
            serializer = OTPVerifySerailizer(data=request.data)

            # valid i/p format
            if not serializer.is_valid():
                return Response(
                    serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            username = serializer.validated_data['username']
            otp = serializer.validated_data['otp']

            # get user & profile
            try:
                user=User.objects.get(username=username)
                profile = user.profile
            except (User.DoesNotExist, UserProfile.DoesNotExist):
                return Response(
                    {'error':'User not found'},
                    status=status.HTTP_404_NOT_FOUND
                )

            # check if otp exists
            if not profile.otp_code:
                return Response(
                    {'error':'No OTP found. Please request a new one.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # check if otp expired (5 mins)
            if not is_otp_valid(profile):
                # clear expired otp
                profile.otp_code = None
                profile.otp_created_at = None
                profile.save()

                return Response(
                    {'error':'OTP expired. Please login again.'},
                    status = status.HTTP_400_BAD_REQUEST
                )
            
            # Verify Otp matches
            if profile.otp_code!=otp:
                return Response(
                    {'error':'Invalid OTP'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Otp valid 
            print(f"OTP verified for {username}")

            # clear otp (one time use)
            profile.otp_code = None
            profile.otp_created_at = None
            profile.save()

            # generate jwt tokens
            refresh = RefreshToken.for_user(user)

            return Response({
                'access': str(refresh.access_token),
                'refresh': str(refresh),
                'username': user.username,
                'email': user.email
            }, status=status.HTTP_200_OK)

