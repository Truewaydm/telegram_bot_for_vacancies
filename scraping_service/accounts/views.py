from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model

from accounts.forms import UserLoginForm, UserRegistrationForm, UserUpdateForm, ContactForm
from django.contrib import messages

from scraping.models import Errors
import datetime

# Create your views here.

User = get_user_model()


def login_view(request):
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        data = form.cleaned_data
        email = data.get('email')
        password = data.get('password')
        user = authenticate(request, email=email, password=password)
        login(request, user)
        return redirect('home')
    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('home')


def register_view(request):
    form = UserRegistrationForm(request.POST or None)
    if form.is_valid():
        new_user = form.save(commit=False)  # encrypt password
        new_user.set_password(form.cleaned_data['password'])
        new_user.save()
        messages.success(request, 'User added to the system')
        return render(request, 'accounts/register_done.html', {'new_user': new_user})
    return render(request, 'accounts/register.html', {'form': form})


def update_view(request):
    contact_form = ContactForm()
    if request.user.is_authenticated:
        user = request.user
        if request.method == 'POST':
            form = UserUpdateForm(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                user.city = data['city']
                user.language = data['language']
                user.send_email = data['send_email']
                user.save()
                return redirect('accounts:update')
        form = UserUpdateForm(
            initial={
                'city': user.city,
                'language': user.language,
                'send_email': user.send_email
            })
        return render(request, 'accounts/update.html', {'form': form, 'contact_form': contact_form})
    else:
        return redirect('accounts:login')


def delete_view(request):
    if request.user.is_authenticated:
        user = request.user
        if request.method == 'POST':
            query_set = User.objects.get(pk=user.pk)
            query_set.delete()
            messages.error(request, 'User deleted')
    return redirect('home')


def contact_view(request):
    if request.method == 'POST':
        contact_form = ContactForm(request.POST or None)
        if contact_form.is_valid():
            data = contact_form.cleaned_data
            city = data.get('city')
            language = data.get('language')
            email = data.get('email')
            query_set_errors = Errors.objects.filter(timestamp=datetime.date.today())
            if query_set_errors.exists():
                error = query_set_errors.first()
                # It's work if DB have only 1 objects in all list data = error.data_errors.get('user_data', [])
                # Else DB have 2 or more objects, code have Exception list' object has no attribute 'get'
                data = error.data_errors.get('user_data', [])
                data.append({'city': city, 'email': email, 'language': language})
                error.data_errors['user_data'] = data
                error.save()
            else:
                data = {'user_data': [
                    {'city': city, 'email': email, 'language': language}
                ]}
                Errors(data=data).save()
            messages.success(request, 'The data has been sent to the administration.')
            return redirect('accounts:update')
        else:
            return redirect('accounts:update')
    else:
        return redirect('accounts:login')