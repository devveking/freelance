from django.db import models
from accounting.models import CustomUser  # Импорт кастомного пользователя


class Job(models.Model):
    STATUS_CHOICES = [
        ('new', 'Активное'),
        ('in_progress', 'В процессе'),
        ('completed', 'Завершено'),
    ]

    title = models.CharField(max_length=255, verbose_name="Заголовок")
    description = models.TextField(verbose_name="Описание")
    budget = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Бюджет")
    deadline = models.DateField(verbose_name="Крайний срок")
    category = models.CharField(max_length=100, verbose_name="Категория")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new', verbose_name="Статус")

    client = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="jobs", verbose_name="Клиент")
    tags = models.CharField(max_length=255, blank=True, verbose_name="Теги")  # Теги через запятую


    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def __str__(self):
        return self.title
