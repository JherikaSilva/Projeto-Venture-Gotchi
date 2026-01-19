from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib import messages
import logging

logger = logging.getLogger(__name__)


# =======================================
# LOGIN VIEW — LOGIN MODERNO E SEGURO
# =======================================
def login_view(request):
    """
    Tela de login customizada usando Bootstrap.
    Valida credenciais, exibe erros e redireciona ao dashboard.
    """

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            messages.success(request, "Login realizado com sucesso!")
            logger.info(f"LOGIN: Usuário '{username}' entrou no sistema.")
            return redirect("home")
        else:
            messages.error(request, "Usuário ou senha inválidos.")
            logger.warning(f"TENTATIVA DE LOGIN FALHOU PARA '{username}'.")

    return render(request, "accounts/login.html")


# =======================================
# LOGOUT VIEW
# =======================================
def logout_view(request):
    """
    Realiza logout de forma segura e limpa.
    """
    logout(request)
    messages.info(request, "Você saiu da sua conta.")
    return redirect("login")


# =======================================
# HOME VIEW — DASHBOARD (CLASS-BASED VIEW)
# =======================================
class HomeView(LoginRequiredMixin, TemplateView):
    """
    Dashboard principal do usuário contendo:
    - nível
    - XP atual
    - XP para o próximo nível
    - porcentagem de progresso
    """

    template_name = "accounts/home.html"
    login_url = "login"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        # Proteção contra campos nulos
        xp = getattr(user, "xp", 0)
        level = getattr(user, "level", 1)
        next_level_xp = level * 100

        # Porcentagem do progresso
        if next_level_xp == 0:
            progress_percent = 0
        else:
            progress_percent = int((xp / next_level_xp) * 100)

        # Enviar tudo organizado ao template
        context["profile"] = {
            "user": user,
            "xp": xp,
            "level": level,
            "next_level_xp": next_level_xp,
            "progress_percent": progress_percent,
        }

        logger.info(f"HOME ACESSADA → {user.username}")

        return context


# =======================================
# PROFILE VIEW — PERFIL COMPLETO
# =======================================
class ProfileView(LoginRequiredMixin, TemplateView):
    """
    Página do perfil com:
    - avatar
    - nome
    - email
    - bio
    - interesses
    - XP e nível
    """

    template_name = "accounts/profile.html"
    login_url = "login"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        context["profile"] = {
            "username": user.username,
            "full_name": user.get_full_name(),
            "email": user.email,
            "bio": getattr(user, "bio", ""),
            "interests": getattr(user, "interests", ""),
            "avatar": user.avatar.url if hasattr(user, "avatar") and user.avatar else None,
            "xp": getattr(user, "xp", 0),
            "level": getattr(user, "level", 1),
            "next_level_xp": getattr(user, "level", 1) * 100,
            "progress_percent": int((getattr(user, "xp", 0) / (getattr(user, "level", 1) * 100)) * 100),
        }

        logger.info(f"PERFIL ACESSADO → {user.username}")

        return context
