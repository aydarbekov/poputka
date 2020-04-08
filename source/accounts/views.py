from django.contrib.auth import login
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView
from accounts.forms import SignUpForm, UpdateForm, ProfileForm_2, UserChangePasswordForm
from accounts.models import Profiles
from webapp.forms import ReviewForm


class SignUp(CreateView):
    form_class = SignUpForm
    second_form_class = ProfileForm_2
    template_name = 'user_create.html'

    def get_context_data(self, **kwargs):
        context = super(SignUp, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class()
        if 'form2' not in context:
            context['form2'] = self.second_form_class()
        return context

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        form2 = self.second_form_class(request.POST, self.request.FILES)

        if form.is_valid() and form2.is_valid():
            return self.form_valid(form, form2)
        return self.form_invalid(form, form2)

    def form_valid(self, form, form2):
        self.object = form.save(commit=True)
        self.object.save()
        self.prof = form2.save(commit=False)
        self.prof.user = self.object
        self.prof.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, form2):
        return self.render_to_response(self.get_context_data(form=form, form2=form2))

    def get_success_url(self):
        return reverse('accounts:user_detail', kwargs={'pk': self.object.pk})


class UserDetailView(DetailView):
    model = User
    template_name = 'user_detail.html'
    context_object_name = 'user_obj'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        history = set(context['user_obj'].announcement.all() |
                      context['user_obj'].clients.all())
        history = sorted(history, key=lambda O: O.departure_time, reverse=True)
        context['history'] = history
        context['review_form'] = ReviewForm()
        return context


class UserUpdateView(UpdateView):
    model = User
    template_name = 'user_update.html'
    context_object_name = 'user'
    form_class = UpdateForm
    second_form_class = ProfileForm_2

    def get_context_data(self, **kwargs):
        context = super(UserUpdateView, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class(instance=self.object)
        if 'form2' not in context:
            context['form2'] = self.second_form_class(instance=self.object.profile)
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.profile = Profiles.objects.get(pk=self.object.profile.pk)
        form = self.get_form()
        form2 = self.second_form_class(request.POST, self.request.FILES, instance=self.profile)

        if form.is_valid() and form2.is_valid():
            return self.form_valid(form, form2)
        return self.form_invalid(form, form2)

    def form_valid(self, form, form2):
        self.object = form.save(commit=True)
        self.object.save()
        self.profile = form2.save(commit=True)
        profile = form2.save(commit=True)
        profile.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, form2):
        return self.render_to_response(self.get_context_data(form=form, form2=form2))

    def get_success_url(self):
        return reverse('accounts:user_detail', kwargs={'pk': self.object.pk})


class UserPasswordChangeView(UserPassesTestMixin, UpdateView):
    model = User
    template_name = 'user_password_change.html'
    form_class = UserChangePasswordForm
    context_object_name = 'user_obj'

    def test_func(self):
        return self.get_object() == self.request.user

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('accounts:login')


class UserDeleteView(DeleteView):
    template_name = 'user_delete.html'
    model = User
    success_url = reverse_lazy('webapp:index')
