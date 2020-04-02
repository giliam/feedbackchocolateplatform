from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, reverse
from django.views.decorators.debug import sensitive_post_parameters

from protocole1 import forms


@login_required
def homepage(request):
    return render(request, "homepage.html", {})


##
# USER PAGES
##


@sensitive_post_parameters("password")
def log_in(request):
    error = False
    if request.method == "POST":
        form = forms.ConnectionForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data[
                "username"
            ]  # Nous récupérons le nom d'profile_user
            password = form.cleaned_data["password"]  # … et le mot de passe
            user = authenticate(
                username=username, password=password
            )  # Nous vérifions si les données sont correctes
            if user:  # Si l'objet renvoyé n'est pas None
                login(request, user)  # nous connectons l'profile_user
                return redirect("homepage")
            else:  # sinon une erreur sera affichée
                error = True
    else:
        if request.user.is_authenticated:
            return redirect("homepage")
        form = forms.ConnectionForm()
    return render(
        request,
        "users_login.html",
        {"form": form, "user": request.user, "error": error},
    )


@login_required
def log_out(request):
    logout(request)
    return redirect(reverse(log_in))
