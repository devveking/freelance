
# userprofile/models.py

from django.db import models
from accounting.models import CustomUser

class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
    first_name = models.CharField(max_length=30, null=True, blank=True)  # Добавлено поле для first_name
    role = models.CharField(null=True,max_length=100, blank=True)
    bio = models.TextField(null=True,blank=True)
    gender = models.CharField(null=True,max_length=10, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    location = models.CharField(null=True,max_length=100, blank=True)
    skills = models.CharField(null=True,max_length=255, blank=True)  # Можно хранить как CSV или использовать ManyToMany
    categories = models.CharField(null=True,max_length=255, blank=True)
    hourly_rate = models.PositiveIntegerField(null=True, blank=True)
    project_rate = models.PositiveIntegerField(null=True, blank=True)

    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)
    background_image = models.ImageField(upload_to='profile_backgrounds/', null=True, blank=True)

    # Дополнительно опыт работы и образование можно вынести в отдельные модели
    def __str__(self):
        return f"Профиль {self.user.username}"

class WorkExperience(models.Model):
    profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='experiences')
    company = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    period = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return f"{self.company} — {self.role}"

class Education(models.Model):
    profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='educations')
    institution = models.CharField(max_length=100)
    specialization = models.CharField(max_length=100)
    period = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.institution}"


class Portfolio(models.Model):
    profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='portfolios')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='portfolio_images/', null=True, blank=True)
    pdf = models.FileField(upload_to='portfolio_pdfs/', null=True, blank=True)  # добавили это поле
    link = models.URLField(blank=True)

    def __str__(self):
        return self.title


class Review(models.Model):
    profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='reviews')
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('profile', 'author')  # Prevent duplicate reviews by the same author

    def str(self):
        return f"{self.author.username} → {self.profile.user.username} ({self.rating}★)"