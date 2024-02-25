from django.contrib.auth.models import User
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import AuthenticationFailed

from .permissions import IsAuthenticateAndAccountOwner
from .serializers import UserSerializer, UserRegisterSerializer, UserLogoutSerializer


class UserDetailView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticateAndAccountOwner]
    http_method_names = ['get', 'patch']

    def get_object(self):
        """
        Returns the object the view is displaying.

        You may want to override this if you need to provide non-standard
        queryset lookups.  Eg if objects are referenced using multiple
        keyword arguments in the url conf.
        """
        user = self.request.user.id

        obj = get_object_or_404(User, id=user)

        # May raise a permission denied
        self.check_object_permissions(self.request, obj)

        return obj

    @swagger_auto_schema(
        operation_description='Retrieve current user details. Current user can only retrieve their own details.',
        responses={200: UserSerializer, 404: 'Not Found'}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description='Update current user details. Current user can only update their own details.',
        request_body=UserSerializer,
        responses={200: UserSerializer, 400: 'Bad Request'}
    )
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class LoginView(APIView):
    permission_classes = []

    @swagger_auto_schema(
        operation_description='Login to the system, returns access and refresh tokens',
        request_body=UserRegisterSerializer,
        responses={200: 'OK', 400: 'Bad Request'}
    )
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({'detail': f'Account with username: {username} not found'},
                            status=status.HTTP_400_BAD_REQUEST)
        if not user.check_password(password):
            raise AuthenticationFailed('Invalid password')
        refresh = RefreshToken.for_user(user)
        return Response(status=status.HTTP_200_OK, data={
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })


class RegisterView(APIView):
    permission_classes = []

    @swagger_auto_schema(
        operation_description='Register a new user',
        request_body=UserRegisterSerializer,
        responses={201: 'Created', 400: 'Bad Request'}
    )
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            try:
                serializer.save()
            except Exception as e:
                return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({'detail': 'Account not created. Please check the field names and values and try again.'},
                        status=status.HTTP_400_BAD_REQUEST)


class LogoutView(generics.GenericAPIView):
    serializer_class = UserLogoutSerializer
    permission_classes = (IsAuthenticated, )

    @swagger_auto_schema(
        operation_description='Logout from the system',
        request_body=UserLogoutSerializer,
        responses={204: 'No Content', 400: 'Bad Request'}
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
