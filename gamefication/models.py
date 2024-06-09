from django.db import models
# from django.contrib.auth.models import User

# class Leaderboard(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     points = models.IntegerField(default=0)
#     rank = models.IntegerField(default=0)

#     def __str__(self):
#         return f"{self.user.username} - Rank: {self.rank}, Points: {self.points}"

# class Badge(models.Model):
#     name = models.CharField(max_length=100)
#     description = models.TextField()
#     criteria = models.CharField(max_length=200)
#     icon_url = models.URLField()

#     def __str__(self):
#         return self.name

# class UserBadge(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     badge = models.ForeignKey(Badge, on_delete=models.CASCADE)
#     date_awarded = models.DateField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.user.username} - {self.badge.name}"

# class Challenge(models.Model):
#     name = models.CharField(max_length=100)
#     description = models.TextField()
#     criteria = models.CharField(max_length=200)
#     reward = models.CharField(max_length=100)
#     duration = models.DurationField()

#     def __str__(self):
#         return self.name

# class UserProgress(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE)
#     progress_status = models.CharField(max_length=50)

#     def __str__(self):
#         return f"{self.user.username} - {self.challenge.name} - {self.progress_status}"

# class Duel(models.Model):
#     challenger = models.ForeignKey(User, related_name='challenger', on_delete=models.CASCADE)
#     opponent = models.ForeignKey(User, related_name='opponent', on_delete=models.CASCADE)
#     challenge_type = models.CharField(max_length=100)
#     challenge_details = models.TextField()
#     winner = models.ForeignKey(User, related_name='winner', on_delete=models.SET_NULL, null=True, blank=True)
#     date_conducted = models.DateField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.challenger.username} vs {self.opponent.username}"
