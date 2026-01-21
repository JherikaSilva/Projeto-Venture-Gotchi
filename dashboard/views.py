from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from missions.models import Mission

@login_required
def dashboard_home(request):
    user = request.user

    missions = (
        Mission.objects
        .filter(user=user, completed=False)
        .prefetch_related("subtasks")
        .order_by("-created_at")
    )

    context = {
        "missions": missions,
        "xp": user.xp,
        "level": user.level,
        "xp_percentage": user.xp_percentage,  # usa seu @property do User
        "xp_next": user.xp_for_next_level(),  # usa seu método do User
    }
    return render(request, "dashboard/home.html", context)
