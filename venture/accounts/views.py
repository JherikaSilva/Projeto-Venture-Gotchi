from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
import logging

logger = logging.getLogger(__name__)



def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'accounts/login.html', {
                'error': 'Usuário ou senha incorretos'
            })

    return render(request, 'accounts/login.html')



def logout_view(request):
    logout(request)
    return redirect('login')




class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/home.html'
    login_url = 'login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        xp = getattr(user, 'xp', 0)
        level = getattr(user, 'level', 1)
        
        next_level_xp = level * 100
        progress_percent = min((xp / next_level_xp) * 100, 100)

        context['profile'] = {
            'user': user,
            'xp': xp,
            'level': level,
            'next_level_xp': next_level_xp,
            'progress_percent': int(progress_percent),
        }

        logger.info(f"HOME ACESSADA — usuário: {user.username}")
        return context




class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/profile.html'
    login_url = 'login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        context['profile'] = {
            'username': user.username,
            'full_name': user.get_full_name(),
            'email': user.email,
            'bio': getattr(user, 'bio', ''),
            'interests': getattr(user, 'interests', ''),
            'avatar': user.avatar.url if hasattr(user, 'avatar') and user.avatar else None,
            'xp': getattr(user, 'xp', 0),
            'level': getattr(user, 'level', 1),
        }

        logger.info(f"PERFIL ACESSADO — usuário: {user.username}")
        return context
