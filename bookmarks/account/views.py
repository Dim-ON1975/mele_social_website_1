# Представления аккаунта пользователя.
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from .forms import LoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm
from django.contrib.auth.decorators import login_required
from .models import Profile
from django.contrib import messages


def user_login(request):
    """
    Форма аутентификации пользователя на сайте (в базе данных)
    :param request: Объект, хранящий информацию о запросе, object.
    :return: HTML-страницу 'account/login.html'
    """
    if request.method == 'POST':
        # Экземпляр формы с переданными данными.
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            # Аутентификация пользователя по базе данных.
            # Если пользователя нет в базе, то вернётся None.
            user = authenticate(request,
                                username=cd['username'],
                                password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Аутентификация прошла успешно')
                else:
                    # Пользователь не активен
                    return HttpResponse('Отключенная учетная запись')
            else:
                # Пользователя не существует в базе.
                return HttpResponse('Неверный логин или пароль')
        else:
            # Форма не валидна.
            return HttpResponse('Необходимо заполнить все поля формы')
    else:
        # Экземпляр новой формы для входа (метод GET)
        form = LoginForm()
    return render(request, 'account/login.html', {'form': form})


@login_required
def dashboard(request):
    """
    Отображение информационной панели при входе пользователей в свои учетные записи.
    """
    return render(request,
                  'account/dashboard.html',
                  {'section': 'dashboard'})


def register(request):
    """
    Регистрация пользователя.
    :param request: Объект, хранящий информацию о запросе, object.
    :return: HTML-страницы 'account/register_done.html' или 'account/register.html'
    """
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Создать новый объект пользователя,
            # но пока не сохранять его
            new_user = user_form.save(commit=False)
            # Установить выбранный пароль: хеширование при помощи .set_password
            new_user.set_password(user_form.cleaned_data['password'])
            # Сохранить объект User
            new_user.save()
            # Создать профиль пользователя
            Profile.objects.create(user=new_user)
            return render(request,
                          'account/register_done.html',
                          {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request,
                  'account/register.html',
                  {'user_form': user_form})


@login_required
def edit(request):
    """
    Редактирование пользователями личной информации.
    :param request: Объект, хранящий информацию о запросе, object.
    :return: HTML-страница 'account/edit.html'
    """
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            # Сообщения для пользователя
            messages.success(request, 'Профиль обновлён успешно')
        else:
            messages.success(request, 'Ошибка при обновлении профиля')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request,
                  'account/edit.html',
                  {'user_form': user_form,
                   'profile_form': profile_form})

