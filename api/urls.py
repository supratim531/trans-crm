from .views import *
from django.contrib import admin
from rest_framework import routers
from django.urls import path, include

router = routers.DefaultRouter()
router.register(r'customers', CustomerViewset)

urlpatterns = [
    path('api/register/', Register.as_view(), name='register'),
    path('api/login/', Login.as_view(), name='login'),
    path('api/logout/', Logout.as_view(), name='logout'),
    path('api/employee/', EmployeeView.as_view(), name='employee'),
    path('api/', include(router.urls))
]
