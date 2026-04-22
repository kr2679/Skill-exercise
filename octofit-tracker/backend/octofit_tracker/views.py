from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from django.contrib.auth.models import User
from .models import Team, Activity, Leaderboard, Workout, UserProfile
from .serializers import (
    UserSerializer, UserDetailSerializer, UserProfileSerializer,
    TeamSerializer, ActivitySerializer, LeaderboardSerializer, WorkoutSerializer
)


class UserViewSet(viewsets.ModelViewSet):
    """ViewSet for User management"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['username', 'email', 'first_name', 'last_name']

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return UserDetailSerializer
        return UserSerializer

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def me(self, request):
        """Get current authenticated user"""
        serializer = UserDetailSerializer(request.user)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def activities(self, request, pk=None):
        """Get user's activities"""
        user = self.get_object()
        activities = user.activities.all()
        serializer = ActivitySerializer(activities, many=True)
        return Response(serializer.data)


class UserProfileViewSet(viewsets.ModelViewSet):
    """ViewSet for UserProfile management"""
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return UserProfile.objects.filter(user=self.request.user)

    @action(detail=False, methods=['get', 'put'], permission_classes=[IsAuthenticated])
    def my_profile(self, request):
        """Get or update current user's profile"""
        profile, created = UserProfile.objects.get_or_create(user=request.user)
        if request.method == 'PUT':
            serializer = self.get_serializer(profile, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        serializer = self.get_serializer(profile)
        return Response(serializer.data)


class TeamViewSet(viewsets.ModelViewSet):
    """ViewSet for Team management"""
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'description']

    def perform_create(self, serializer):
        """Set owner when creating team"""
        serializer.save(owner=self.request.user)

    def perform_update(self, serializer):
        """Update team"""
        serializer.save()

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def add_member(self, request, pk=None):
        """Add a member to the team"""
        team = self.get_object()
        user_id = request.data.get('user_id')
        try:
            user = User.objects.get(id=user_id)
            team.members.add(user)
            return Response({'status': 'member added'}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def remove_member(self, request, pk=None):
        """Remove a member from the team"""
        team = self.get_object()
        user_id = request.data.get('user_id')
        try:
            user = User.objects.get(id=user_id)
            team.members.remove(user)
            return Response({'status': 'member removed'}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)


class ActivityViewSet(viewsets.ModelViewSet):
    """ViewSet for Activity logging"""
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['activity_type', 'user__username']
    ordering_fields = ['date', 'created_at', 'calories_burned']
    ordering = ['-date']

    def get_queryset(self):
        """Filter activities by user"""
        user = self.request.query_params.get('user')
        queryset = Activity.objects.all()
        if user:
            queryset = queryset.filter(user__username=user)
        return queryset

    def perform_create(self, serializer):
        """Set user when creating activity"""
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['get'])
    def my_activities(self, request):
        """Get current user's activities"""
        activities = Activity.objects.filter(user=request.user)
        serializer = self.get_serializer(activities, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Get user activity statistics"""
        user = request.query_params.get('user', request.user.id)
        activities = Activity.objects.filter(user_id=user)
        total_calories = sum(a.calories_burned for a in activities)
        total_distance = sum(a.distance or 0 for a in activities)
        total_activities = activities.count()
        return Response({
            'total_calories': total_calories,
            'total_distance': total_distance,
            'total_activities': total_activities,
        })


class LeaderboardViewSet(viewsets.ModelViewSet):
    """ViewSet for Leaderboard"""
    queryset = Leaderboard.objects.all()
    serializer_class = LeaderboardSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['rank', 'total_calories', 'total_distance']
    ordering = ['rank']

    @action(detail=False, methods=['get'])
    def team_leaderboard(self, request):
        """Get leaderboard for a specific team"""
        team_id = request.query_params.get('team_id')
        if team_id:
            leaderboards = Leaderboard.objects.filter(team_id=team_id).order_by('rank')
            serializer = self.get_serializer(leaderboards, many=True)
            return Response(serializer.data)
        return Response({'error': 'team_id is required'}, status=status.HTTP_400_BAD_REQUEST)


class WorkoutViewSet(viewsets.ModelViewSet):
    """ViewSet for Workout management"""
    queryset = Workout.objects.all()
    serializer_class = WorkoutSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'description', 'difficulty']
    ordering_fields = ['created_at', 'difficulty']
    ordering = ['-created_at']

    def get_queryset(self):
        """Filter workouts by user"""
        user = self.request.query_params.get('user')
        queryset = Workout.objects.all()
        if user:
            queryset = queryset.filter(user__username=user)
        return queryset

    def perform_create(self, serializer):
        """Set user when creating workout"""
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['get'])
    def my_workouts(self, request):
        """Get current user's workouts"""
        workouts = Workout.objects.filter(user=request.user)
        serializer = self.get_serializer(workouts, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def by_difficulty(self, request):
        """Get workouts by difficulty level"""
        difficulty = request.query_params.get('level')
        if difficulty:
            workouts = Workout.objects.filter(difficulty=difficulty)
            serializer = self.get_serializer(workouts, many=True)
            return Response(serializer.data)
        return Response({'error': 'level parameter is required'}, status=status.HTTP_400_BAD_REQUEST)
