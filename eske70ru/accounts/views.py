from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from .forms import RegistrationForm, LoginForm
from .models import CustomUser


def register(request):
    """Регистрация"""
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # Пользователь не активен до подтверждения email
            user.save()

            # Отправка email с подтверждением
            current_site = get_current_site(request)
            mail_subject = 'Активируйте ваш аккаунт'
            message = render_to_string('accounts/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()

            return redirect('confirm_email')
    else:
        form = RegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})

def activate(request, uidb64, token):
    """Активация аккаунта"""
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.is_verified = True
        user.save()
        login(request, user)
        return redirect('home')
    else:
        return render(request, 'accounts/activation_invalid.html')


def confirm_email(request):
    """Подтверждение email"""
    return render(request, 'accounts/confirm_email.html')


def login_view(request):
    """Аутентификация пользователя"""
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password, is_verified=True)
            if user is not None:
                login(request, user)
                return redirect('home')  # Перенаправление на главную страницу
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    """Выход из аккаунта"""
    logout(request)
    return redirect('home')  # Перенаправление на главную страницу


def profile(request):
    """
    Профиль пользователя
    """
    if request.user.is_authenticated:
        # user = CustomUser.objects.get(pk=pk)
        context = {
            'title': f'Профиль {request.user}',
            'user': request.user}
        return render(request, 'accounts/profile.html', context)
    else:
        return redirect('home')
    return render(request,'accounts/profile.html')
