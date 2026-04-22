from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Team(models.Model):
    """Team model for team management"""
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_teams')
    members = models.ManyToManyField(User, related_name='joined_teams', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'teams'

    def __str__(self):
        return self.name


class Activity(models.Model):
    """Activity logging model"""
    ACTIVITY_TYPES = (
        ('running', 'Running'),
        ('cycling', 'Cycling'),
        ('swimming', 'Swimming'),
        ('walking', 'Walking'),
        ('gym', 'Gym'),
        ('sports', 'Sports'),
        ('other', 'Other'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activities')
    activity_type = models.CharField(max_length=20, choices=ACTIVITY_TYPES)
    duration = models.IntegerField(help_text="Duration in minutes")
    calories_burned = models.IntegerField()
    distance = models.FloatField(null=True, blank=True, help_text="Distance in kilometers")
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    date = models.DateField(default=timezone.now)

    class Meta:
        db_table = 'activities'
        ordering = ['-date', '-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.activity_type}"


class Leaderboard(models.Model):
    """Leaderboard for competitive tracking"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='leaderboard')
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='leaderboards')
    total_calories = models.IntegerField(default=0)
    total_distance = models.FloatField(default=0.0)
    total_activities = models.IntegerField(default=0)
    rank = models.IntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'leaderboards'
        ordering = ['rank']

    def __str__(self):
        return f"{self.user.username} - Rank {self.rank}"


class Workout(models.Model):
    """Workout suggestions and plans"""
    DIFFICULTY_LEVELS = (
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='workouts')
    title = models.CharField(max_length=200)
    description = models.TextField()
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_LEVELS)
    duration = models.IntegerField(help_text="Duration in minutes")
    exercises = models.JSONField(default=list, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'workouts'
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class UserProfile(models.Model):
    """Extended user profile"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True)
    profile_picture = models.URLField(blank=True)
    fitness_goals = models.TextField(blank=True)
    preferred_activities = models.JSONField(default=list, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'user_profiles'

    def __str__(self):
        return f"{self.user.username} Profile"
