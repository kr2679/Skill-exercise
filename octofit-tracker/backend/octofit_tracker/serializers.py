from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Team, Activity, Leaderboard, Workout, UserProfile


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model"""
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
        read_only_fields = ['id']


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer for UserProfile model"""
    user = UserSerializer(read_only=True)

    class Meta:
        model = UserProfile
        fields = ['id', 'user', 'bio', 'profile_picture', 'fitness_goals', 'preferred_activities', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class TeamSerializer(serializers.ModelSerializer):
    """Serializer for Team model"""
    owner = UserSerializer(read_only=True)
    members = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Team
        fields = ['id', 'name', 'description', 'owner', 'members', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class ActivitySerializer(serializers.ModelSerializer):
    """Serializer for Activity model with ObjectId to string conversion"""
    user = UserSerializer(read_only=True)

    class Meta:
        model = Activity
        fields = ['id', 'user', 'activity_type', 'duration', 'calories_burned', 'distance', 'description', 'created_at', 'date']
        read_only_fields = ['id', 'created_at']


class LeaderboardSerializer(serializers.ModelSerializer):
    """Serializer for Leaderboard model"""
    user = UserSerializer(read_only=True)
    team = TeamSerializer(read_only=True)

    class Meta:
        model = Leaderboard
        fields = ['id', 'user', 'team', 'total_calories', 'total_distance', 'total_activities', 'rank', 'updated_at']
        read_only_fields = ['id', 'updated_at']


class WorkoutSerializer(serializers.ModelSerializer):
    """Serializer for Workout model"""
    user = UserSerializer(read_only=True)

    class Meta:
        model = Workout
        fields = ['id', 'user', 'title', 'description', 'difficulty', 'duration', 'exercises', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class UserDetailSerializer(serializers.ModelSerializer):
    """Detailed user serializer with profile and stats"""
    profile = UserProfileSerializer(read_only=True)
    activities = ActivitySerializer(many=True, read_only=True)
    workouts = WorkoutSerializer(many=True, read_only=True)
    leaderboard = LeaderboardSerializer(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'profile', 'activities', 'workouts', 'leaderboard']
        read_only_fields = ['id']
