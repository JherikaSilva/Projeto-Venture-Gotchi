from django.db import models
from django.conf import settings


class Achievement(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="achievements"
    )
    code = models.CharField(max_length=50)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=200, blank=True, default="")
    earned_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "code")

    def __str__(self):
        return f"{self.user} - {self.title}"


class ActivityEvent(models.Model):
    """
    Histórico do usuário (feed).
    Serve para:
    - Dashboard: histórico
    - Dashboard: gráficos (XP por dia)
    - Dashboard: sugestões
    """
    EVENT_TYPES = [
        ("subtask_completed", "Subtarefa concluída"),
        ("mission_completed", "Missão concluída"),
        ("level_up", "Subiu de nível"),
        ("achievement", "Conquista desbloqueada"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="activity_events",
    )

    event_type = models.CharField(max_length=30, choices=EVENT_TYPES)
    message = models.CharField(max_length=220)

    xp_delta = models.IntegerField(default=0)  # ganho/perda de XP (normalmente ganho)
    track = models.CharField(max_length=10, blank=True, default="")  # prog/ux/biz/soft

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.event_type} - {self.created_at}"
