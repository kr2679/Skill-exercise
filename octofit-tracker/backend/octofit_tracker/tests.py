from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from .models import Team, Activity, Leaderboard, Workout, UserProfile
from .serializers import (
    UserSerializer, UserProfileSerializer, TeamSerializer,
    ActivitySerializer, LeaderboardSerializer, WorkoutSerializer
)


class UserModelTest(TestCase):
    """Test User model and profile"""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )

    def test_user_creation(self):
        """Test user is created successfully"""
        self.assertEqual(self.user.username, 'testuser')
        self.assertEqual(self.user.email, 'test@example.com')

    def test_user_profile_creation(self):
        """Test user profile creation"""
        profile = UserProfile.objects.create(
            user=self.user,
            bio='Test bio',
            fitness_goals='Get fit'
        )
        self.assertEqual(profile.user, self.user)
        self.assertEqual(profile.bio, 'Test bio')


class TeamModelTest(TestCase):
    """Test Team model"""

    def setUp(self):
        self.user = User.objects.create_user(
            username='teamowner',
            email='owner@example.com',
            password='testpass123'
        )
        self.team = Team.objects.create(
            name='Test Team',
            description='A test team',
            owner=self.user
        )

    def test_team_creation(self):
        """Test team is created successfully"""
        self.assertEqual(self.team.name, 'Test Team')
        self.assertEqual(self.team.owner, self.user)

    def test_add_team_member(self):
        """Test adding member to team"""
        member = User.objects.create_user(
            username='member',
            email='member@example.com',
            password='testpass123'
        )
        self.team.members.add(member)
        self.assertIn(member, self.team.members.all())


class ActivityModelTest(TestCase):
    """Test Activity model"""

    def setUp(self):
        self.user = User.objects.create_user(
            username='activeuser',
            email='active@example.com',
            password='testpass123'
        )

    def test_activity_creation(self):
        """Test activity is created successfully"""
        activity = Activity.objects.create(
            user=self.user,
            activity_type='running',
            duration=30,
            calories_burned=300,
            distance=5.0
        )
        self.assertEqual(activity.user, self.user)
        self.assertEqual(activity.activity_type, 'running')
        self.assertEqual(activity.calories_burned, 300)


class WorkoutModelTest(TestCase):
    """Test Workout model"""

    def setUp(self):
        self.user = User.objects.create_user(
            username='workoutuser',
            email='workout@example.com',
            password='testpass123'
        )

    def test_workout_creation(self):
        """Test workout is created successfully"""
        workout = Workout.objects.create(
            user=self.user,
            title='Morning Run',
            description='5K morning run',
            difficulty='beginner',
            duration=30,
            exercises=['warm up 5min', 'run 25min']
        )
        self.assertEqual(workout.title, 'Morning Run')
        self.assertEqual(workout.difficulty, 'beginner')


class UserSerializerTest(TestCase):
    """Test User serializer"""

    def setUp(self):
        self.user = User.objects.create_user(
            username='serializertest',
            email='serializer@example.com',
            password='testpass123',
            first_name='John',
            last_name='Doe'
        )

    def test_user_serializer(self):
        """Test user serializer"""
        serializer = UserSerializer(self.user)
        data = serializer.data
        self.assertEqual(data['username'], 'serializertest')
        self.assertEqual(data['email'], 'serializer@example.com')


class ActivitySerializerTest(TestCase):
    """Test Activity serializer"""

    def setUp(self):
        self.user = User.objects.create_user(
            username='activitytest',
            email='activity@example.com',
            password='testpass123'
        )
        self.activity = Activity.objects.create(
            user=self.user,
            activity_type='cycling',
            duration=45,
            calories_burned=400,
            distance=15.0
        )

    def test_activity_serializer(self):
        """Test activity serializer"""
        serializer = ActivitySerializer(self.activity)
        data = serializer.data
        self.assertEqual(data['activity_type'], 'cycling')
        self.assertEqual(data['calories_burned'], 400)


class TeamSerializerTest(TestCase):
    """Test Team serializer"""

    def setUp(self):
        self.user = User.objects.create_user(
            username='teamtest',
            email='team@example.com',
            password='testpass123'
        )
        self.team = Team.objects.create(
            name='Serializer Team',
            description='Test team for serializer',
            owner=self.user
        )

    def test_team_serializer(self):
        """Test team serializer"""
        serializer = TeamSerializer(self.team)
        data = serializer.data
        self.assertEqual(data['name'], 'Serializer Team')
        self.assertEqual(data['owner']['username'], 'teamtest')


class UserAPITest(APITestCase):
    """Test User API endpoints"""

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='apitest',
            email='apitest@example.com',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)

    def test_get_users(self):
        """Test getting users list"""
        response = self.client.get('/api/users/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_current_user(self):
        """Test getting current user"""
        response = self.client.get('/api/users/me/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class ActivityAPITest(APITestCase):
    """Test Activity API endpoints"""

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='activityapi',
            email='activityapi@example.com',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)

    def test_create_activity(self):
        """Test creating an activity"""
        data = {
            'activity_type': 'swimming',
            'duration': 60,
            'calories_burned': 500,
            'distance': 2.0
        }
        response = self.client.post('/api/activities/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_activities(self):
        """Test getting activities list"""
        response = self.client.get('/api/activities/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TeamAPITest(APITestCase):
    """Test Team API endpoints"""

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='teamapi',
            email='teamapi@example.com',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)

    def test_create_team(self):
        """Test creating a team"""
        data = {
            'name': 'API Test Team',
            'description': 'Team created via API'
        }
        response = self.client.post('/api/teams/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_teams(self):
        """Test getting teams list"""
        response = self.client.get('/api/teams/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
