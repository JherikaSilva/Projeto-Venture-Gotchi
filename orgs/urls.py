from django.urls import path
from .views import team_dashboard
from .views import (
    team_dashboard,
    corporate_track_create,
    corporate_track_list,
    assign_track_to_team,
    corporate_mission_create,
    corporate_mission_complete,
)



urlpatterns = [
    path("team/", team_dashboard, name="team_dashboard"),
    path("tracks/", corporate_track_list, name="corporate_track_list"),
    path("tracks/new/", corporate_track_create, name="corporate_track_create"),
    path("tracks/<int:track_id>/assign/", assign_track_to_team, name="assign_track_to_team"),
    path("tracks/<int:track_id>/missions/new/",corporate_mission_create,name="corporate_mission_create"),
    path("missions/<int:mission_id>/complete/",corporate_mission_complete,name="corporate_mission_complete"),

]
