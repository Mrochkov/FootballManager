from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect, render
from django.contrib import messages

@login_required
def custom_logout(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect("Table")

def custom_login(request):
    if request.user.is_authenticated:
        return redirect('Table')

    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Hello <b>{user.username}</b>! You have been logged in")
                return redirect('Table')
            else:
                messages.error(request, "Nieprawidłowa nazwa użytkownika lub hasło.")
        else:
            messages.error(request, "Wprowadzono nieprawidłowe dane.")

    else:
        form = AuthenticationForm()

    return render(
        request=request,
        template_name="users/login.html",
        context={'form': form}
    )