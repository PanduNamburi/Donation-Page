from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Intern(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    referral_code = models.CharField(max_length=50, unique=True)
    total_donations_raised = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    goal_amount = models.DecimalField(max_digits=10, decimal_places=2, default=2000.00)
    points = models.IntegerField(default=0)
    rank = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.referral_code}"

    def calculate_rank(self):
        """Calculate rank based on total donations raised"""
        all_interns = Intern.objects.order_by('-total_donations_raised')
        for i, intern in enumerate(all_interns, 1):
            if intern.id == self.id:
                self.rank = i
                self.save()
                return i
        return 0

    def calculate_points(self):
        """Calculate points based on performance"""
        points = int(self.total_donations_raised / 10)  # 1 point per $10 raised
        self.points = points
        self.save()
        return points

class Donation(models.Model):
    intern = models.ForeignKey(Intern, on_delete=models.CASCADE, related_name='donations')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    donor_name = models.CharField(max_length=100, blank=True)
    donor_email = models.EmailField(blank=True)
    message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"${self.amount} donation to {self.intern.user.get_full_name()}"

class Achievement(models.Model):
    ACHIEVEMENT_TYPES = [
        ('first_donation', 'First Donation'),
        ('goal_reached', 'Goal Reached'),
        ('top_performer', 'Top Performer'),
        ('streak', 'Streak Master'),
        ('social_butterfly', 'Social Butterfly'),
    ]
    
    intern = models.ForeignKey(Intern, on_delete=models.CASCADE, related_name='achievements')
    achievement_type = models.CharField(max_length=20, choices=ACHIEVEMENT_TYPES)
    title = models.CharField(max_length=100)
    description = models.TextField()
    icon = models.CharField(max_length=50, default='🏆')
    unlocked_at = models.DateTimeField(auto_now_add=True)
    is_unlocked = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.title} - {self.intern.user.get_full_name()}"

class Notification(models.Model):
    NOTIFICATION_TYPES = [
        ('achievement', 'Achievement Unlocked'),
        ('donation', 'New Donation'),
        ('milestone', 'Milestone Reached'),
        ('rank_change', 'Rank Change'),
    ]
    
    intern = models.ForeignKey(Intern, on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    title = models.CharField(max_length=100)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.intern.user.get_full_name()}"


