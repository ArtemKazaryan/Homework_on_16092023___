from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate


def signupuser(request):
    if request.method == 'GET':
        return render(request, 'user/signupuser.html', {'form': UserCreationForm})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(
                    request.POST['username'],
                    password=request.POST['password1']
                )
                user.save()
            except IntegrityError:
                return render(request, 'user/signupuser.html', {'form': UserCreationForm(),
                                                                'error': 'Пользователь с таким именем существует!'})
            else:
                login(request, user)
                return redirect('shop:product_list')
        else:
            return render(request, 'user/signupuser.html',
                          {'form': UserCreationForm(),
                           'error': 'Пароли не совпали'})


def loginuser(request):
    if request.method == 'GET':
        return render(request, 'user/loginuser.html', {'form': AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'],
                            password=request.POST['password'])
        if user is None:
            return render(request, 'user/loginuser.html',
                          {'form': AuthenticationForm(),
                           'error': 'Неверные данные для входа!'})
        else:
            login(request, user)
            return redirect('shop:product_list')


@login_required()
def user_profile(request, pk):
    return render(request, 'user/user_profile.html')


@login_required
def logoutuser(request):
    logout(request)
    return redirect('user:login')
