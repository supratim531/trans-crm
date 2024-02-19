from .models import *
from rest_framework import serializers
from django.contrib.auth.models import User

class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = '__all__'

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class RegisterSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=100)
    email = serializers.EmailField()
    username = serializers.CharField(max_length=100)
    password = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=50)

    # def get_fields(self):
    #     fields = super().get_fields()
    #     exclude_fields = self.context.get('exclude_fields', ['password'])

    #     for field in exclude_fields:
    #         # providing a default prevents a KeyError
    #         # if the field does not exist
    #         fields.pop(field, default=None)

    #     return fields

    def create(self, validated_data):
        # Extracting role_id
        role = Role.objects.get(role_name="staff")
        serializedData = RoleSerializer(role)
        role_id = serializedData.data["role_id"]

        # Extracting team_id
        team = Team.objects.get(team_name=validated_data['last_name'])
        serializedData = TeamSerializer(team)
        team_id = serializedData.data["team_id"]

        user = User.objects.create_user(validated_data['username'], validated_data['email'], validated_data['password'])
        employee = Employee(None, validated_data['username'], validated_data['first_name'], validated_data['email'], team_id, role_id)
        employee.save()
        return user

# class RegisterSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['id', 'first_name', 'last_name', 'email', 'username', 'password']
#         extra_kwargs = {"password": {"write_only": True}}

#     def create(self, validated_data):
#         role = Role.objects.get(role_name="staff")
#         serializedData = RoleSerializer(role)
#         role_id = serializedData.data["role_id"]
#         user = User.objects.create_user(validated_data['username'], validated_data['email'], validated_data['password'])
#         employee = Employee(validated_data['username'], f"{validated_data['first_name']} {validated_data['last_name']}", validated_data['email'], team_id, role_id)
#         employee.save()
#         return user

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'
