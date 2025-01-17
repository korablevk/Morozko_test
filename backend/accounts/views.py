from django.contrib import messages
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, TemplateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django_email_verification import send_email

from cart.models import Cart

from .forms import ProfileForm, UserRegistrationForm, UserLoginForm
from .models import User


class UserLoginView(LoginView):
    template_name = 'accounts/login.html'
    form_class = UserLoginForm

    def get_success_url(self):
        redirect_page = self.request.POST.get('next', None)
        if redirect_page and redirect_page != reverse('user:logout'):
            return redirect_page
        return reverse_lazy('main:index')

    def form_valid(self, form):

        session_key = self.request.session.session_key
        user = form.get_user()

        if user:
            auth.login(self.request, user)
            if session_key:

                forgot_carts = Cart.objects.filter(user=user)
                if forgot_carts.exists():
                    forgot_carts.delete()

                Cart.objects.filter(session_key=session_key).update(user=user)
                messages.success(self.request, "Successfully logged in!")
                return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):

        messages.error(self.request, 'Username or Password is incorrect')
        return self.render_to_response(self.get_context_data(form=form))



class UserRegistrationView(CreateView):
    template_name = 'accounts/registration.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('account:email_verification_sent')

    def form_valid(self, form):
        session_key = self.request.session.session_key
        user = form.save(commit=False)
        user_email = form.cleaned_data.get('email')
        user_username = form.cleaned_data.get('username')
        user_password = form.cleaned_data.get('password1')

        user = User.objects.create_user(
            username=user_username, email=user_email, password=user_password
        )

        user.is_active = False

        send_email(user)

        if session_key:
            Cart.objects.filter(session_key=session_key).update(user=user)

        return HttpResponseRedirect(self.success_url)


class UserProfileView(LoginRequiredMixin, UpdateView):
    template_name = 'accounts/profile.html'
    form_class = ProfileForm
    success_url = reverse_lazy('account:profile')

    def get_object(self, queryset=None):
        return self.request.user
    
    def form_valid(self, form):
        messages.success(self.request, "Профайл успешно обновлен")
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, "Произошла ошибка")
        return super().form_invalid(form)


@login_required
def logout(request):
    messages.success(request, f"{request.user.username}, Вы вышли из аккаунта")
    auth.logout(request)
    return redirect(reverse('main:index'))


class UserCartView(TemplateView):
    template_name = 'accounts/accounts_cart.html'