from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .forms import RegisterForm, LoginForm
from .models import User
from django.http import HttpResponseForbidden

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration successful. Please login.")
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})

@login_required
def admin_dashboard(request):
    users = User.objects.all()
    return render(request, 'accounts/dashboard_admin.html', {'users': users})

@login_required
def moderator_dashboard(request):
    return render(request, 'accounts/dashboard_moderator.html')

@login_required
def user_dashboard(request):
    return render(request, 'accounts/dashboard_user.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)

            # redirect based on role
            if user.role == 'admin':
                return redirect('admin_dashboard')
            elif user.role == 'moderator':
                return redirect('moderator_dashboard')
            else:
                return redirect('user_dashboard')

        messages.error(request, "Invalid username or password.")
    return render(request, 'accounts/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def dashboard_view(request):
    if request.user.role != 'admin':
        return HttpResponseForbidden("You are not allowed to access this page.")
    users = User.objects.all()
    return render(request, 'accounts/dashboard.html', {'users': users})


@login_required
@user_passes_test(lambda u: u.role == 'admin')
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if user != request.user:
        user.delete()
        messages.success(request, f"Deleted user {user.username}")
    else:
        messages.error(request, "You cannot delete yourself.")
    return redirect('dashboard')
