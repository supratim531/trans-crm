import io
from .serializers import *
from rest_framework import status
from django.db import transaction
from rest_framework import viewsets
from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, TokenAuthentication

class Register(APIView):
    @transaction.atomic
    def post(self, request):
        try:
            serializer = RegisterSerializer(data=request.data)

            if serializer.is_valid():
                user = serializer.save()
                serializedData = RegisterSerializer(user)
                token = Token.objects.create(user=user)

                return Response({
                    "message": f"User {serializer.data['username']} is created",
                    "token": token.key,
                    "user": serializedData.data
                }, status=status.HTTP_201_CREATED)
            else:
                return Response({
                    "error": serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                "message": str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

class Login(APIView):
    def post(self, request):
        try:
            username = request.data['username']
            password = request.data['password']

            if not User.objects.filter(username=username).exists():
                return Response({
                    "message": "Username doesn't exist"
                }, status=status.HTTP_401_UNAUTHORIZED)
            
            user = User.objects.get(username=username)

            if not user.check_password(password):
                return Response({
                    "message": "Wrong credential"
                }, status=status.HTTP_401_UNAUTHORIZED)

            token, created = Token.objects.get_or_create(user=user)
            serializer = UserSerializer(user)

            return Response({
                "message": "Login successful",
                "token": token.key
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                "message": str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

class Logout(APIView):
    def post(self, request):
        try:
            token_key = request.headers.get('Authorization').split()[1]
            token = Token.objects.get(key=token_key)
            token.delete()

            return Response({
                "message": "Successfully logged out"
            }, status=status.HTTP_200_OK)

        except Token.DoesNotExist:
            return Response({
                "message": "Invalid token"
            }, status=status.HTTP_401_UNAUTHORIZED)

        except Exception as e:
            return Response({
                "message": str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

class CustomerViewset(viewsets.ModelViewSet):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = CustomerSerializer
    queryset = Customer.objects.all()

    def get_queryset(self):
        if self.request.user.is_authenticated:
            serializedData = EmployeeSerializer(Employee.objects.filter(emp_username=self.request.user), many=True)
            stream = io.BytesIO(JSONRenderer().render(serializedData.data))
            employeeSet = JSONParser().parse(stream)
            role_id = employeeSet[0]["role"]
            team_id = employeeSet[0]["team"]

            # Fetch role_name from role_id
            serializedData = RoleSerializer(Role.objects.get(role_id=role_id))
            role = serializedData.data
            role_name = role["role_name"]

            if role_name == "SUPER_ADMIN":
                return Customer.objects.all()
            elif role_name == "ADMIN":
                return Customer.objects.filter(team=employeeSet[0]["team"])
            else:
                return Customer.objects.filter(employee=employeeSet[0]["emp_id"])

class EmployeeView(APIView):
    def delete(self, request):
        if self.request.user.is_authenticated:
            serializedData = EmployeeSerializer(Employee.objects.filter(emp_username=self.request.user), many=True)
            stream = io.BytesIO(JSONRenderer().render(serializedData.data))
            employeeSet = JSONParser().parse(stream)
            role_id = employeeSet[0]["role"]

            # Fetch role_name from role_id
            serializedData = RoleSerializer(Role.objects.get(role_id=role_id))
            role = serializedData.data
            role_name = role["role_name"]

            payload = request.data
            username = payload.get("username", None)

            if username is not None:
                if role_name == "SUPER_ADMIN":
                    user = User.objects.filter(username=username)
                    employee = Employee.objects.filter(emp_username=username)
                    employee.delete()
                    flag, _ = user.delete()

                    if flag != 0:
                        return Response({
                            "message": f"User {username} deleted successfully"
                        }, status=status.HTTP_200_OK)
                    else:
                        return Response({
                            "error": f"Username {username} not found"
                        }, status=status.HTTP_404_NOT_FOUND)
            else:
                return Response({
                    "error": f"Username is not provided"
                }, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            "error": f"Permission denied"
        }, status=status.HTTP_403_FORBIDDEN)
