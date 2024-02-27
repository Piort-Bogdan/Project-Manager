from django.contrib.auth.models import User
from drf_spectacular.utils import extend_schema, OpenApiExample
from rest_framework.generics import get_object_or_404, GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import AuthenticationFailed

from .permissions import IsAuthenticateAndAccountOwner
from .serializers import UserSerializer, UserRegisterSerializer, UserLogoutSerializer, LoginResponseSerializer, \
    UserErrorSerializer


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

    @extend_schema(
           description='Retrieve current user details. Current user can only retrieve their own details.',
           responses={200: UserSerializer, 404: UserErrorSerializer}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(
        description='Update current user details. Current user can only update their own details.',
        request=UserSerializer,
        responses={200: UserSerializer, 400: UserErrorSerializer},
        examples=[
            OpenApiExample('Example 1', summary='Update user details', value={
                'username': 'user1', 'email': 'user@example.com', 'first_name': 'User', 'last_name': 'One'})
        ],
    )
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class LoginView(GenericAPIView):
    permission_classes = []

    @extend_schema(
        description='Login to the system',
        responses={200: LoginResponseSerializer(many=False), 400: UserErrorSerializer}
    )
    @extend_schema(
        request=LoginResponseSerializer,
        examples=[
            OpenApiExample('Example 1', summary='Login with username and password', value={
                'username': 'user1', 'password': 'password123'}),
        ],
    )
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        if username is None:
            return Response({'detail': 'Username is required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({'detail': f'Account with username: {username} not found'},
                            status=status.HTTP_400_BAD_REQUEST)
        if not user.check_password(password):
            raise AuthenticationFailed('Invalid password')
        refresh = RefreshToken.for_user(user)
        serializer = LoginResponseSerializer({
            'refresh': str(refresh),
            'access': str(refresh.access_token)})
        return Response(status=status.HTTP_200_OK, data=serializer.data)


class RegisterView(GenericAPIView):
    permission_classes = []

    @extend_schema(
        description='Register a new user',
        request=UserRegisterSerializer,
        responses={201: UserRegisterSerializer, 400: UserErrorSerializer},
        examples=[
            OpenApiExample('Example 1', summary='Register a new user', value={
                'username': 'user1', 'email': 'user1@example.ru', 'password': 'password'}),
        ],
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

    @extend_schema(
        description='Logout from the system',
        responses={204: "No content", 400: UserErrorSerializer},
        examples=[
            OpenApiExample('Example 1', summary='Logout from the system', value={'refresh_token': 'refresh_token'}),
        ],
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
