from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView

from accounts.forms import SignUpForm, ProfileForm, UserForm
from accounts.models import Profile


class SignUpView(CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('login')
    template_name = 'accounts/sign_up.html'

    def form_valid(self, form):
        user = form.save()
        Profile.objects.create(user=user)
        return super(SignUpView, self).form_valid(form)


def profile(request):
    current_user = request.user
    if not current_user.is_authenticated:
        return HttpResponseRedirect(reverse_lazy('login'))
    context = {'profile': Profile.objects.get(user=current_user)}
    return render(request, 'accounts/profile.html', context)


def change_profile(request):
    current_user = request.user
    if not current_user.is_authenticated:
        return HttpResponseRedirect(reverse_lazy('login'))

    if request.method != 'POST':
        user_form = UserForm(instance=current_user)
        profile_form = ProfileForm(instance=current_user.profile)
    else:
        user_form = UserForm(request.POST, instance=current_user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=current_user.profile)
        if user_form.is_valid():
            user_form.save()
            return HttpResponseRedirect(reverse_lazy('profile'))
        if profile_form.is_valid():
            profile_form.save()
            return HttpResponseRedirect(reverse_lazy('profile'))

    context = {'user_form': user_form, 'profile_form': profile_form}
    return render(request, 'accounts/change_profile.html', context)


def change_avatar(request):
    current_user = request.user
    if not current_user.is_authenticated:
        return HttpResponseRedirect(reverse_lazy('login'))

    if request.method != 'POST':
        return HttpResponseRedirect('profile')

    uploaded_file = request.FILES['file']
    current_user.profile.avatar = uploaded_file
    current_user.profile.save()
    response = HttpResponse()
    response.status_code = 200
    return response
