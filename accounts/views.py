from django.contrib.auth.models import User
from django.views.generic.edit import CreateView
from django.shortcuts import redirect, render
from django.contrib.auth.views import LoginView
from .forms import SignUpForm
from .models import OneCode
from app.models import Customer


class SignUp(CreateView):
    model = User
    form_class = SignUpForm
    success_url = '/accounts/confirm_signup'
    template_name = 'registration/signup.html'


def confirm_signup(request):
    if request.method == "POST":
        code = request.POST.get("code")
        if OneCode.objects.filter(code=code).exists():
            user = OneCode.objects.get(code=code).user
            user.is_active = True
            user.save()
            OneCode.objects.filter(code=code).delete()
            Customer.objects.create(user=user, nickname=user.username)
            return redirect("/accounts/login/")
        return render(request, 'registration/confirm_error.html')
    return render(request, 'registration/confirm_signup.html')


class ProfileView(LoginView):
    def get_success_url(self):
        return 'http://127.0.0.1:8000/profile/'



