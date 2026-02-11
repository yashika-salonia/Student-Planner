from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView 
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils import timezone
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.shortcuts import redirect
import threading

from .serializers import UserSerializer, OTPVerifySerailizer
from .models import UserProfile
from .utils import generate_otp, send_otp_email,send_verification_email , is_otp_valid

@method_decorator(csrf_exempt, name='dispatch')
class RegisterView(generics.CreateAPIView):
    
    """POST /api/register/ -> Register a new user"""
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
            
        # create user
        response= super().create(request, *args, **kwargs)
    
        # get created user
        user=User.objects.get(username=request.data.get('username'))
        profile=user.profile

        # send mail for verification
        def send_email_async():
            send_verification_email(
                user.email,
                user.username,
                profile.verification_token
            )

        thread=threading.Thread(target=send_email_async)
        thread.daemon=True
        thread.start()

        return Response(
            {
                'success':True,
                'message':'Registeration successful! Please check your mail to verify your account',
                'email':user.email,
                'user':response.data
            },
            status =status.HTTP_201_CREATED
        )
    
@method_decorator(csrf_exempt, name='dispatch')
class VerifyEmailView(APIView):
    """Verify email via link """

    def get(self, request, token):
        try:
            profile=UserProfile.objects.get(verification_token=token)

            # check if already verified
            if profile.email_verified:
                return redirect(f'http://localhost:5173/login?verified=already')
            
            profile.email_verified=True
            profile.save()

            print(f"Email verified for user: {profile.user.username}")

            return redirect(f'http://localhost:5173/login?verified=true&username={profile.user.username}')
        
        except UserProfile.DoesNotExist:
            return redirect('http://localhost:5173/login?verified=false')

@method_decorator(csrf_exempt, name='dispatch')
class ResendVerificationView(APIView):
    """REsend verification email"""

    def post(self, request):
        email=request.data.get('email')

        if not email:
            return Response(
                {'error':'Email required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            user=User.objects.get(email=email)
            profile=user.profile

            # check if already verified
            if profile.email_verified:
                return Response(
                    {'message':'Email already verified. Yoou can login now.'},
                    status=status.HTTP_200_OK
                )
            
            # send mail again
            def send_email_async():
                send_verification_email(
                    user.email,
                    user.username,
                    profile.verification_token
                )
            
            thread=threading.Thread(target=send_email_async)
            thread.daemon = True
            thread.start()

            return Response(
                {
                    'success': True,
                    'message':f'Verification email sent to {email}. Please check your inbox.'
                },
                status=status.HTTP_200_OK
            )
        except User.DoesNotExist:
            return Response(
                {'error':'No account found with this email'},
                status=status.HTTP_404_NOT_FOUND
            )

@method_decorator(csrf_exempt, name='dispatch')
class LoginStep1View(APIView):
    """
    Step 1:Verify username/password, email verified and send OTP
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
        
        profile=user.profile

        if not profile.email_verified:
            return Response(
                {
                    'error':'Email not verified',
                    'message':f'Please check {user.email} and click the verification link to verify your account to continue.',
                    'email':user.email,
                    'verification_required':True
                },
                status=status.HTTP_403_FORBIDDEN
            )

        # generate OTP
        otp_code=generate_otp()
        print(f"Generated OTP for {username}: {otp_code}")

        # save OTP and timestamp to database
        profile.otp_code = otp_code
        profile.otp_created_at = timezone.now()
        profile.save()

        # send OTP to user's email
        def send_otp_async():
            send_otp_email(user.email, otp_code)

        # if not email_sent:
        #     profile.otp_code=None
        #     profile.otp_created_at=None
        #     profile.save()
        thread=threading.Thread(target=send_otp_async)
        thread.daemon=True
        thread.start()
        
        return Response({
            'status':'otp_sent',
            'message':f'OTP sent to {user.email}',
            'username':username,
            'email':user.email
        }, status=status.HTTP_200_OK)

@method_decorator(csrf_exempt, name='dispatch')
class LoginStep2View(APIView):
        """Step 2: Verify OTP and issue JWT tokens"""

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
            if profile.otp_code != otp:
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

