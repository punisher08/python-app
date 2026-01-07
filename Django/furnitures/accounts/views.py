from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .forms import RegisterForm
from .models import User
from django.http import HttpResponseForbidden
from django.conf import settings

from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import RegisterForm


def register_view(request):
    if request.user.is_authenticated:
        if request.user.is_superuser or request.user.role == 'admin':
            return redirect('/admin/')
        return redirect('/')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration successful. Please login.")
            return redirect('login')
        else:
            for field, errors in form.errors.items():
                label = form.fields[field].label if field in form.fields else field
                for error in errors:
                    messages.error(request, f"{label}: {error}")
    else:
        form = RegisterForm()

    return render(request, 'accounts/register.html', {'form': form})

# ---------------------- DASHBOARDS ---------------------- #
@login_required
@user_passes_test(lambda u: u.is_superuser)
def admin_dashboard(request):
    return render(request, 'accounts/dashboard_admin.html')


@login_required
def moderator_dashboard(request):
    return render(request, 'accounts/dashboard_moderator.html')


@login_required
def user_dashboard(request):
    return render(request, 'accounts/dashboard_user.html')


# ---------------------- LOGIN ---------------------- #
def login_view(request):
    # Redirect logged-in users away from login page
    if request.user.is_authenticated:
        if request.user.is_superuser or request.user.role == 'admin':
            return redirect('/admin/')
        else:
            return redirect('user_dashboard')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            # Redirect based on role or superuser
            if user.is_superuser or user.role == 'admin':
                return redirect('/admin/')
            else:
                return redirect('user_dashboard')

        messages.error(request, "Invalid username or password.")
    return render(request, 'accounts/login.html')


# ---------------------- LOGOUT ---------------------- #
def logout_view(request):
    logout(request)
    return redirect('login')


# ---------------------- ADMIN MANAGEMENT ---------------------- #
@login_required
def dashboard_view(request):
    if not (request.user.is_superuser or request.user.role == 'admin'):
        return HttpResponseForbidden("You are not allowed to access this page.")
    users = User.objects.all()
    return render(request, 'accounts/dashboard.html', {'users': users})


@login_required
@user_passes_test(lambda u: u.is_superuser or u.role == 'admin')
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if user != request.user:
        user.delete()
        messages.success(request, f"Deleted user {user.username}")
    else:
        messages.error(request, "You cannot delete yourself.")
    return redirect('dashboard')
