from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.db.models import Sum, Avg, Count
from .services import get_user_team
from .models import TeamMembership, CorporateTrack, Team, TeamTrackAssignment
from .forms import CorporateTrackForm



def is_mentor_or_company(user) -> bool:

    return getattr(user, "role_approved", False) and getattr(user, "requested_role", "user") in ("mentor", "company")


@login_required
def team_dashboard(request):
    if not request.user.role_approved:
        return redirect("dashboard")

    team = get_user_team(request.user)
    if not team:
        return render(request, "orgs/team_dashboard.html", {"no_team": True})

    members = TeamMembership.objects.filter(team=team).select_related("user")

    total_xp = members.aggregate(total=Sum("user__xp"))["total"] or 0
    avg_xp = members.aggregate(avg=Avg("user__xp"))["avg"] or 0

    goals = team.goals.all()
    goals_done = goals.filter(is_completed=True).count()
    goals_total = goals.count()

    # 🔹 NOVO: trilhas atribuídas à equipe
    tracks = TeamTrackAssignment.objects.filter(team=team).select_related("track")

    context = {
        "team": team,
        "members": members,
        "total_xp": total_xp,
        "avg_xp": int(avg_xp),
        "goals": goals,
        "goals_done": goals_done,
        "goals_total": goals_total,
        "tracks": tracks,
        "no_team": False,
    }

    return render(request, "orgs/team_dashboard.html", context)

@login_required
def corporate_track_create(request):
    if not request.user.role_approved:
        return redirect("dashboard")

    if request.method == "POST":
        form = CorporateTrackForm(request.POST)
        if form.is_valid():
            track = form.save(commit=False)
            track.created_by = request.user
            track.company = request.user.company  # se você usa relação direta
            track.save()
            return redirect("corporate_track_list")
    else:
        form = CorporateTrackForm()

    return render(request, "orgs/corporate_track_form.html", {"form": form}) 


@login_required
def corporate_track_list(request):
    if not request.user.role_approved:
        return redirect("dashboard")

    tracks = CorporateTrack.objects.filter(created_by=request.user)

    return render(
        request,
        "orgs/corporate_track_list.html",
        {"tracks": tracks}
    )


@login_required
def assign_track_to_team(request, track_id):
    if not request.user.role_approved:
        return redirect("dashboard")

    track = get_object_or_404(CorporateTrack, id=track_id)
    teams = Team.objects.all()  # depois você filtra por empresa

    if request.method == "POST":
        team_id = request.POST.get("team_id")
        team = get_object_or_404(Team, id=team_id)
        TeamTrackAssignment.objects.get_or_create(
            team=team,
            track=track
        )
        return redirect("corporate_track_list")

    return render(
        request,
        "orgs/assign_track.html",
        {"track": track, "teams": teams}
    )

@login_required
def corporate_mission_create(request, track_id):
    if not request.user.role_approved:
        return redirect("dashboard")

    track = get_object_or_404(CorporateTrack, id=track_id)

    if request.method == "POST":
        form = CorporateMissionForm(request.POST)
        if form.is_valid():
            mission = form.save(commit=False)
            mission.track = track
            mission.save()
            return redirect("corporate_track_list")
    else:
        form = CorporateMissionForm()

    return render(
        request,
        "orgs/corporate_mission_form.html",
        {"form": form, "track": track}
    )

@login_required
def corporate_mission_complete(request, mission_id):
    mission = get_object_or_404(CorporateMission, id=mission_id)

    from orgs.services import complete_corporate_mission
    complete_corporate_mission(request.user, mission)

    messages.success(
        request,
        f"Missão '{mission.title}' concluída! XP ganho: {mission.xp_reward}"
    )
    return redirect("team_dashboard")
