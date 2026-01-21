from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.conf import settings

class Mission(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='missions')
    title = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    priority = models.IntegerField(default=1, choices=[
        (1, 'Baixa'),
        (2, 'Média'),
        (3, 'Alta'),
    ])
    mission_xp = models.IntegerField(default=50)
    deadline = models.DateField(null=True, blank=True)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(null=True, blank=True)


    def __str__(self):
        return self.title

    @property
    def progress(self):
        total = self.subtasks.count()
        if total == 0:
            return 0
        done = self.subtasks.filter(completed=True).count()
        return int((done / total) * 100)

    def check_completion(self):
        if self.progress == 100:
            self.completed = True
            self.save()

    def clean(self):
        if self.deadline and self.deadline < self.created_at.date():
            raise ValidationError("A data limite não pode ser anterior à criação.")


class SubTask(models.Model):
    mission = models.ForeignKey(Mission, on_delete=models.CASCADE, related_name="subtasks")
    title = models.CharField(max_length=150)
    xp_reward = models.IntegerField(default=10)
    completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
