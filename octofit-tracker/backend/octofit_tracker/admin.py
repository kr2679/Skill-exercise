from django.contrib import admin
from .models import Team, Activity, Leaderboard, Workout, UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """Admin interface for UserProfile"""
    list_display = ['user', 'created_at', 'updated_at']
    search_fields = ['user__username', 'user__email']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    """Admin interface for Team"""
    list_display = ['name', 'owner', 'created_at', 'updated_at']
    search_fields = ['name', 'owner__username']
    filter_list = ['created_at']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Team Information', {
            'fields': ('name', 'description', 'owner')
        }),
        ('Members', {
            'fields': ('members',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    """Admin interface for Activity"""
    list_display = ['user', 'activity_type', 'date', 'duration', 'calories_burned']
    search_fields = ['user__username', 'activity_type']
    filter_list = ['activity_type', 'date', 'created_at']
    readonly_fields = ['created_at']
    fieldsets = (
        ('Activity Details', {
            'fields': ('user', 'activity_type', 'date')
        }),
        ('Activity Stats', {
            'fields': ('duration', 'calories_burned', 'distance')
        }),
        ('Additional Info', {
            'fields': ('description',)
        }),
        ('Timestamps', {
            'fields': ('created_at',)
        }),
    )


@admin.register(Leaderboard)
class LeaderboardAdmin(admin.ModelAdmin):
    """Admin interface for Leaderboard"""
    list_display = ['user', 'team', 'rank', 'total_calories', 'total_distance']
    search_fields = ['user__username', 'team__name']
    filter_list = ['team', 'rank']
    readonly_fields = ['updated_at']
    fieldsets = (
        ('User & Team', {
            'fields': ('user', 'team')
        }),
        ('Stats', {
            'fields': ('total_calories', 'total_distance', 'total_activities', 'rank')
        }),
        ('Timestamps', {
            'fields': ('updated_at',)
        }),
    )


@admin.register(Workout)
class WorkoutAdmin(admin.ModelAdmin):
    """Admin interface for Workout"""
    list_display = ['title', 'user', 'difficulty', 'duration', 'created_at']
    search_fields = ['title', 'user__username']
    filter_list = ['difficulty', 'created_at']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Workout Information', {
            'fields': ('user', 'title', 'difficulty')
        }),
        ('Workout Details', {
            'fields': ('description', 'duration', 'exercises')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )
