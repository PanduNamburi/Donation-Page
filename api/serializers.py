from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Intern, Donation, Achievement, Notification

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']

class InternSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    full_name = serializers.SerializerMethodField()
    progress_percentage = serializers.SerializerMethodField()
    
    class Meta:
        model = Intern
        fields = ['id', 'user', 'full_name', 'referral_code', 'total_donations_raised', 
                 'goal_amount', 'points', 'rank', 'progress_percentage', 'created_at']
    
    def get_full_name(self, obj):
        return obj.user.get_full_name()
    
    def get_progress_percentage(self, obj):
        if obj.goal_amount > 0:
            return min((obj.total_donations_raised / obj.goal_amount) * 100, 100)
        return 0

class DonationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Donation
        fields = ['id', 'amount', 'donor_name', 'donor_email', 'message', 'created_at']

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'notification_type', 'title', 'message', 'is_read', 'created_at']

class LeaderboardSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Intern
        fields = ['rank', 'full_name', 'referral_code', 'total_donations_raised', 'points']
    
    def get_full_name(self, obj):
        return obj.user.get_full_name() 