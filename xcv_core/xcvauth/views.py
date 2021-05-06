from .forms import ChangePasswordForm, CustomAuthenticationForm
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect, reverse
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView


def home(request):
    data = {
        "canonical": reverse('xcvauth:home')
    }
    return render(request, 'home.html', data)


def logout_request(request):
    logout(request)
    # messages.info(request, "Logged out successfully!")
    return redirect("/")


def login_request(request):
    next_path = request.GET.get('next')
    if request.user.is_authenticated:
        return redirect(settings.LOGIN_REDIRECT_URL)

    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                # messages.info(request, f"You are now logged in as {username}")
                redirect_to = settings.LOGIN_REDIRECT_URL
                if next_path:
                    redirect_to = next_path
                return redirect(redirect_to)
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = CustomAuthenticationForm()
    data = {
        "canonical": reverse('xcvauth:login'),
        "form": form,
    }
    return render(request, 'login.html', data)


class ChangePasswordView(TemplateView):
    form_class = ChangePasswordForm
    template_name = 'change-password.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.update(dict(form=self.form_class(user=self.request.user)))
        ctx['canonical'] = reverse('xcvauth:change_password')
        return ctx

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST, user=request.user)
        if form.is_valid():
            user = request.user
            user.set_password(form.cleaned_data.get('new_password'))
            user.save()
            messages.success(request, "Password changed successfully")
        return render(request, self.template_name, context=dict(form=form))
