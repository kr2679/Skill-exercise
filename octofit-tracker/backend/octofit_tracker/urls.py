"""
URL configuration for octofit_tracker project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import os
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .views import (
    UserViewSet, UserProfileViewSet, TeamViewSet,
    ActivityViewSet, LeaderboardViewSet, WorkoutViewSet
)

# Initialize router
router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'userprofiles', UserProfileViewSet, basename='userprofile')
router.register(r'teams', TeamViewSet, basename='team')
router.register(r'activities', ActivityViewSet, basename='activity')
router.register(r'leaderboards', LeaderboardViewSet, basename='leaderboard')
router.register(r'workouts', WorkoutViewSet, basename='workout')

# API Root view
@api_view(['GET'])
def api_root(request):
    """API root endpoint"""
    return Response({
        'users': request.build_absolute_uri('/api/users/'),
        'teams': request.build_absolute_uri('/api/teams/'),
        'activities': request.build_absolute_uri('/api/activities/'),
        'leaderboards': request.build_absolute_uri('/api/leaderboards/'),
        'workouts': request.build_absolute_uri('/api/workouts/'),
    })

# Codespace environment variable for URLs
codespace_name = os.environ.get('CODESPACE_NAME')
if codespace_name:
    base_url = f"https://{codespace_name}-8000.app.github.dev"
else:
    base_url = "http://localhost:8000"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', api_root, name='api-root'),
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
    path('api/auth/', include('dj_rest_auth.urls')),
    path('api/auth/registration/', include('dj_rest_auth.registration.urls')),
]
