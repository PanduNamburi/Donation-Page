from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.models import Token
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.db import transaction
from django.utils import timezone
import os
import json
from .models import Intern, Donation, Achievement, Notification
from .serializers import (
    InternSerializer, DonationSerializer, 
    NotificationSerializer, LeaderboardSerializer
)

def generate_unique_referral_code(username):
    """Generate a unique referral code for a user"""
    base_referral_code = f"{username.lower()}{timezone.now().year}"
    referral_code = base_referral_code
    counter = 1
    
    # Ensure unique referral code
    while Intern.objects.filter(referral_code=referral_code).exists():
        referral_code = f"{base_referral_code}{counter}"
        counter += 1
    
    return referral_code

@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    """Register a new user and create intern profile"""
    try:
        data = request.data
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        first_name = data.get('first_name', '')
        last_name = data.get('last_name', '')
        
        if User.objects.filter(username=username).exists():
            return Response({'error': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)
        
        if User.objects.filter(email=email).exists():
            return Response({'error': 'Email already exists'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Create user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        
        # Create intern profile
        referral_code = generate_unique_referral_code(username)
        intern = Intern.objects.create(
            user=user,
            referral_code=referral_code
        )
        
        # Create initial achievement
        Achievement.objects.create(
            intern=intern,
            achievement_type='first_donation',
            title='Welcome!',
            description='You\'ve joined the fundraising team!',
            icon='🎉'
        )
        
        # Create token for the user
        token = Token.objects.create(user=user)
        
        return Response({
            'message': 'Registration successful',
            'token': token.key,
            'user_id': user.id,
            'referral_code': referral_code
        }, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    """Login user"""
    try:
        data = request.data
        username = data.get('username')
        password = data.get('password')
        
        user = authenticate(username=username, password=password)
        
        if user is not None:
            # Get or create token for the user
            token, created = Token.objects.get_or_create(user=user)
            
            # Ensure user has an intern profile
            try:
                intern = Intern.objects.get(user=user)
            except Intern.DoesNotExist:
                # Create intern profile if it doesn't exist
                referral_code = generate_unique_referral_code(username)
                intern = Intern.objects.create(
                    user=user,
                    referral_code=referral_code
                )
                print(f"Created intern profile for user {username} with referral code {referral_code}")
            
            return Response({
                'message': 'Login successful',
                'token': token.key,
                'user_id': user.id
            }, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
            
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_user(request):
    """Logout user"""
    try:
        # Delete the user's token
        request.user.auth_token.delete()
        return Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)
    except:
        return Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def intern_data(request):
    """Get current user's intern data"""
    try:
        intern = Intern.objects.get(user=request.user)
        intern.calculate_rank()
        intern.calculate_points()
        
        serializer = InternSerializer(intern)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Intern.DoesNotExist:
        return Response({'error': 'Intern profile not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes([AllowAny])
def leaderboard(request):
    """Get leaderboard data"""
    try:
        interns = Intern.objects.all().order_by('-total_donations_raised')
        
        # Update ranks
        for i, intern in enumerate(interns, 1):
            intern.rank = i
            intern.save()
        
        serializer = LeaderboardSerializer(interns, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def notifications(request):
    """Get user's notifications"""
    try:
        intern = Intern.objects.get(user=request.user)
        notifications = Notification.objects.filter(intern=intern).order_by('-created_at')[:10]
        serializer = NotificationSerializer(notifications, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Intern.DoesNotExist:
        return Response({'error': 'Intern profile not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def mark_notification_read(request, notification_id):
    """Mark notification as read"""
    try:
        intern = Intern.objects.get(user=request.user)
        notification = Notification.objects.get(id=notification_id, intern=intern)
        notification.is_read = True
        notification.save()
        return Response({'message': 'Notification marked as read'}, status=status.HTTP_200_OK)
    except (Intern.DoesNotExist, Notification.DoesNotExist):
        return Response({'error': 'Notification not found'}, status=status.HTTP_404_NOT_FOUND)



@api_view(['POST'])
@permission_classes([AllowAny])
def add_donation(request):
    """Add a donation (public endpoint)"""
    try:
        data = request.data
        referral_code = data.get('referral_code')
        
        try:
            intern = Intern.objects.get(referral_code=referral_code)
        except Intern.DoesNotExist:
            return Response({'error': 'Invalid referral code'}, status=status.HTTP_404_NOT_FOUND)
        
        with transaction.atomic():
            # Create donation
            donation = Donation.objects.create(
                intern=intern,
                amount=data.get('amount'),
                donor_name=data.get('donor_name', 'Anonymous'),
                donor_email=data.get('donor_email', ''),
                message=data.get('message', '')
            )
            
            # Update intern's total
            intern.total_donations_raised += donation.amount
            intern.save()
            
            # Check for achievements
            check_achievements(intern)
            
            # Create notification
            Notification.objects.create(
                intern=intern,
                notification_type='donation',
                title='New Donation!',
                message=f'You received a ${donation.amount} donation!'
            )
        
        return Response({'message': 'Donation added successfully'}, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

def check_achievements(intern):
    """Check and award achievements"""
    # First donation achievement
    if intern.donations.count() == 1:
        Achievement.objects.get_or_create(
            intern=intern,
            achievement_type='first_donation',
            defaults={
                'title': 'First Donation!',
                'description': 'You received your first donation!',
                'icon': '🎉'
            }
        )
    
    # Goal reached achievement
    if intern.total_donations_raised >= intern.goal_amount:
        Achievement.objects.get_or_create(
            intern=intern,
            achievement_type='goal_reached',
            defaults={
                'title': 'Goal Reached!',
                'description': f'You reached your goal of ${intern.goal_amount}!',
                'icon': '🎯'
            }
        )
    
    # Top performer achievement
    if intern.rank <= 3:
        Achievement.objects.get_or_create(
            intern=intern,
            achievement_type='top_performer',
            defaults={
                'title': 'Top Performer!',
                'description': 'You\'re in the top 3 performers!',
                'icon': '🏆'
            }
        )

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_stats(request):
    """Get comprehensive dashboard statistics"""
    try:
        intern = Intern.objects.get(user=request.user)
        intern.calculate_rank()
        intern.calculate_points()
        
        # Get recent donations
        recent_donations = Donation.objects.filter(intern=intern).order_by('-created_at')[:5]
        
        # Get unread notifications count
        unread_notifications = Notification.objects.filter(intern=intern, is_read=False).count()
        
        # Get achievements count
        achievements_count = Achievement.objects.filter(intern=intern, is_unlocked=True).count()
        
        data = {
            'intern': InternSerializer(intern).data,
            'recent_donations': DonationSerializer(recent_donations, many=True).data,
            'unread_notifications': unread_notifications,
            'achievements_count': achievements_count,
            'total_donations_count': intern.donations.count()
        }
        
        return Response(data, status=status.HTTP_200_OK)
    except Intern.DoesNotExist:
        return Response({'error': 'Intern profile not found'}, status=status.HTTP_404_NOT_FOUND)

def serve_static_file(request, filename):
    """Serve static HTML files"""
    static_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static')
    file_path = os.path.join(static_dir, filename)
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return HttpResponse(content, content_type='text/html')
    except FileNotFoundError:
        return HttpResponse('Page not found', status=404)
