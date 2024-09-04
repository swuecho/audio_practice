from django.contrib.auth.models import update_last_login, User
from admin_backend.models import Role, UserRolesRole
from django.db.models import Max, Sum
from django.http import Http404
from rest_framework import generics, permissions, status, viewsets
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from admin_backend.serializers import MyTokenObtainPairSerializer


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        return Response(
            {"data": serializer.validated_data},
        )
    
class RegiserAndObtainPairView(MyTokenObtainPairView):
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response({'error': 'Both username and password are required'}, 
                            status=status.HTTP_400_BAD_REQUEST)

        # Check if user already exists
        if User.objects.filter(username=username).exists():
            return Response({'error': 'Username already exists'}, 
                            status=status.HTTP_400_BAD_REQUEST)

        # Create new user
        user = User.objects.create_user(username=username, password=password)
        user.email = username
        user.save()
        # find OPERATOR role
        role = Role.objects.get(code='OPERATOR')
        # assign role to user
        user_role = UserRolesRole.objects.create(user=user, role=role)
        user_role.save()
        

        # Use the parent class method to get the token
        response = super().post(request, *args, **kwargs)

        if response.status_code == status.HTTP_200_OK:
            return Response(
                {"data": response.data.get("data")},
                status=status.HTTP_201_CREATED,
            )
        return response

class SwitchRoleView(APIView):
    def post(self, request, *args, **kwargs):
        user_and_token = JWTAuthentication().authenticate(request)
        role = request.data["role"]

        if user_and_token is None:
            return Http404  # better
        user = user_and_token[0]

        token = RefreshToken.for_user(user)
        # Add custom claims
        token["role"] = role

        data = {}
        data["refresh"] = str(token)
        data["access"] = str(token.access_token)

        update_last_login(None, user)
        print(data)
        return Response(
            {"data": data},
        )
