from django.db.models import Q
from django.contrib.auth import login
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.views import LoginView
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView, ListView, FormView
from accounts.forms import SignUpForm, UpdateForm, ProfileForm_2, UserChangePasswordForm, FullSearchForm
from accounts.models import User, Profiles
from webapp.forms import ReviewForm
from django.shortcuts import redirect
from django.utils.http import urlencode


class LoginView(LoginView):

    def get_success_url(self):
        # print(self.request.user)
        # print(self.request.user.profile.ban)
        if self.request.user.profile.ban == True:
            raise PermissionDenied("Вы получили бан, доступ к сайту запрещен!")
        return super().get_success_url()


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
        login(self.request, self.object)
        return HttpResponseRedirect(reverse('accounts:user_detail', kwargs={"pk": self.object.pk}))

    def form_invalid(self, form, form2):
        return self.render_to_response(self.get_context_data(form=form, form2=form2))

    def get_success_url(self):
        login(self.request, self.object)
        return HttpResponseRedirect(reverse('accounts:user_detail', kwargs={"pk": self.object.pk}))


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


class UserUpdateView(UserPassesTestMixin, UpdateView):
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
            Profiles.objects.get_or_create(user=self.object)
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

        if form2.cleaned_data['type'] == 'client':
            # print('ddddddddd')
            # print(form2.cleaned_data['car'])
            form2.cleaned_data['car'] = None
            # print(form2.cleaned_data['car'])

            form2.cleaned_data['car_model'] = None
            form2.cleaned_data['car_number'] = None
            form2.cleaned_data['car_seats'] = None
            form2.cleaned_data['status'] = None
            form2.save()

        self.profile = form2.save(commit=True)
        self.profile.save()
        print(form2.cleaned_data['car'])

        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, form2):
        return self.render_to_response(self.get_context_data(form=form, form2=form2))

    def get_success_url(self):
        return reverse('accounts:user_detail', kwargs={'pk': self.object.pk})

    def test_func(self):
        return self.get_object() == self.request.user


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


class UserDeleteView(UserPassesTestMixin, DeleteView):
    template_name = 'user_delete.html'
    model = User
    success_url = reverse_lazy('webapp:index')

    def test_func(self):
        return self.get_object() == self.request.user


class UserListView(UserPassesTestMixin, ListView):
    model = User
    template_name = 'user_list.html'
    context_object_name = 'users'
    paginate_by = 2
    paginate_orphans = 1

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['drivers'] = Profiles.objects.filter(type='driver')
        context['clients'] = Profiles.objects.filter(type='client')
        return context

    def get_queryset(self, *args, **kwargs):
        drivers = self.request.GET.get('drivers')
        clients = self.request.GET.get('clients')
        if drivers:
            return Profiles.objects.filter(Q(type='driver'))
        elif clients:
            return Profiles.objects.filter(Q(type='client'))
        return User.objects.all()

    def test_func(self):
        user = self.request.user
        return user.is_staff


class UserSearchView(FormView):
    template_name = 'search.html'
    form_class = FullSearchForm

    # def test_func(self):
    #     user_requesting = self.request.user
    #     user_detail = User.objects.get(pk=self.kwargs['pk'])
    #     return user_requesting.is_staff or user_requesting.groups.filter(name='principal_staff') or user_detail == user_requesting

    def form_valid(self, form):
        query = urlencode(form.cleaned_data)
        url = reverse('accounts:search_results') + '?' + query
        return redirect(url)


class SearchResultsView(UserPassesTestMixin, ListView):
    model = Profiles
    template_name = 'search.html'
    context_object_name = 'users'
    paginate_by = 2
    paginate_orphans = 1

    def test_func(self):
        user = self.request.user
        return user.is_staff or user.groups.filter(name='principal_staff')

    def get_queryset(self):
        queryset = super().get_queryset()
        form = FullSearchForm(data=self.request.GET)
        if form.is_valid():
            query = self.get_search_query(form)
            queryset = queryset.filter(query).distinct()
        return queryset

    def get_context_data(self, *, object_list=None, group_list=None, text=None, user_list=None, **kwargs):
        form = FullSearchForm(data=self.request.GET)
        if form.is_valid():
            text = form.cleaned_data.get("text")
        query = self.get_query_string()
        users = User.objects.filter(first_name__icontains=text)
        return super().get_context_data(
            form=form, query=query, user_list=users
        )

    def get_query_string(self):
        data = {}
        for key in self.request.GET:
            if key != 'page':
                data[key] = self.request.GET.get(key)
        return urlencode(data)

    def get_search_query(self, form):
        query = Q()
        text = form.cleaned_data.get('text').capitalize()
        if text:
            in_username = form.cleaned_data.get('in_username')
            if in_username:
                query = query | Q(user__username__icontains=text)
            in_first_name = form.cleaned_data.get('in_first_name')
            if in_first_name:
                if "-" in text:
                    first_name, last_name = text.split('-')
                    query = query | Q(user__first_name__icontains=first_name) | Q(user__last_name__icontains=last_name)
                else:
                    query = query | Q(user__first_name__icontains=text)
            in_phone = form.cleaned_data.get('in_phone')
            if in_phone:
                query = query | Q(user__profile__mobile_phone__icontains=text)
        return query