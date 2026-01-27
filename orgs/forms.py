from django import forms
from .models import CorporateTrack, CorporateMission

class CorporateTrackForm(forms.ModelForm):
    class Meta:
        model = CorporateTrack
        fields = ["name", "description", "is_active"]
    
        model = CorporateMission
        fields = ["title", "description", "xp_reward"]






