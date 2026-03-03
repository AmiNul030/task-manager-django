from django.db import models

class Task(models.Model):
    PRIORITY_CHOICES = [
        ("L", "Low"),
        ("M", "Medium"),
        ("H", "High"),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    completed = models.BooleanField(default=False)

    priority = models.CharField(max_length=1, choices=PRIORITY_CHOICES, default="M")
    due_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.title