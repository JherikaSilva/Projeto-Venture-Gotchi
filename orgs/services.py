from django.db.models import Sum
from .models import TeamGoal


def get_user_team(user):
    
    membership = getattr(user, "team_memberships", None)
    if not membership:
        return None
    m = user.team_memberships.select_related("team").first()
    return m.team if m else None


def update_team_goals_on_xp(user, xp_gained: int, subtasks_done: int = 0):
   

    team = get_user_team(user)
    if not team:
        return

    goals = team.goals.all()

    for goal in goals:
        if goal.is_completed:
            continue

        if goal.goal_type == "xp_total":
            goal.current_value += max(int(xp_gained), 0)

        elif goal.goal_type == "missions_done":
            goal.current_value += max(int(subtasks_done), 0)

        goal.check_complete()
        goal.save(update_fields=["current_value", "is_completed", "completed_at"])


def complete_corporate_mission(user, mission):
    
    from .models import CorporateMissionCompletion  # import local pra evitar circular

    completion, created = CorporateMissionCompletion.objects.get_or_create(
        user=user,
        mission=mission
    )
    if not created:
        return False  

    xp = int(getattr(mission, "xp_reward", 0) or 0)

   
    if hasattr(user, "add_xp") and callable(getattr(user, "add_xp")):
        user.add_xp(xp)
    else:
        user.xp = (user.xp or 0) + xp
        user.save(update_fields=["xp"])


    update_team_goals_on_xp(user=user, xp_gained=xp, subtasks_done=1)

    return True
