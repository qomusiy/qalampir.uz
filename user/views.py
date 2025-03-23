from django.shortcuts import render, redirect
from django.views import View
from django.db.models import Q
from .forms import SignUpForm, LoginForm, UpdateUserForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout

# Create your views here.

def singup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  
            user.set_password(form.cleaned_data['password']) 
            user.save()
            login(request, user)
            return redirect('interface')
        else:
            passerror ="Parol noto'g'ri kiritildi."
            return render(request, 'singup.html', {'form': form, 'passerror':passerror})
    else:
        form = SignUpForm()
    return render(request, 'singup.html', {'form': form})

@login_required
def user_update(request):
    if request.method == 'POST':
        form = UpdateUserForm(request.POST, instance=request.user)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password']) 
            user.save()
            form.save()
            login(request, user)
            return redirect('interface')
    else:
        form = UpdateUserForm(instance=request.user)
    return render(request, 'update.html', {'form': form})

@login_required
def user_delete(request):
    if request.method == 'POST':
        user = request.user
        logout(request)  
        user.delete()
        return redirect('index')
    return render(request, 'delete.html')

def user_login(r):
    if r.method == 'POST':
        form = LoginForm(r, data=r.POST)
        if form.is_valid():
            user = form.get_user()
            login(r, user)
            return redirect('interface')
        else:
            passerror = "Parol xato terildi. Parolni unutgan bo'sangiz @qomusiy'ga murojat qiling."
            return render(r, template_name='login.html', context={'form':form, 'passerror':passerror})
    else:
        form = LoginForm()
    return render(r, template_name='login.html', context={'form':form})

def user_logout(r):
    logout(r)
    return redirect('index')