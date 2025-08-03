from django.contrib import admin
from .models import Intern, Donation, Achievement, Notification

@admin.register(Intern)
class InternAdmin(admin.ModelAdmin):
    list_display = ['user', 'referral_code', 'total_donations_raised', 'points', 'rank', 'created_at']
    list_filter = ['created_at', 'rank']
    search_fields = ['user__username', 'user__first_name', 'user__last_name', 'referral_code']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['-total_donations_raised']

@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    list_display = ['intern', 'amount', 'donor_name', 'donor_email', 'created_at']
    list_filter = ['created_at', 'amount']
    search_fields = ['intern__user__username', 'donor_name', 'donor_email']
    readonly_fields = ['created_at']
    ordering = ['-created_at']

@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ['intern', 'achievement_type', 'title', 'is_unlocked', 'unlocked_at']
    list_filter = ['achievement_type', 'is_unlocked', 'unlocked_at']
    search_fields = ['intern__user__username', 'title']
    readonly_fields = ['unlocked_at']
    ordering = ['-unlocked_at']

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['intern', 'notification_type', 'title', 'is_read', 'created_at']
    list_filter = ['notification_type', 'is_read', 'created_at']
    search_fields = ['intern__user__username', 'title', 'message']
    readonly_fields = ['created_at']
    ordering = ['-created_at']


