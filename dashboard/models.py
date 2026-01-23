from django.db import models
from django.conf import settings

class Achievement(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="achievements")
    code = models.CharField(max_length=50)  
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=200, blank=True, default="")
    earned_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "code")

    def __str__(self):
        return f"{self.user} - {self.title}"
