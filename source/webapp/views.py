import csv
import datetime
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.core.exceptions import ValidationError, PermissionDenied
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, DetailView, DeleteView, UpdateView
from django.http import HttpResponseRedirect
from django.urls import reverse
from webapp.forms import ReviewForm, AnnouncementForm
from webapp.models import Announcements, ANNOUNCEMENT_TYPE_CHOICES, REGION_CHOICES, ANNOUNCEMENT_STATUS_CHOICES, \
    ClientsInAnnounce, CarModel, Car, Review
from django.views.generic.base import View


class PassengersList(ListView):
    model = Announcements
    template_name = 'index.html'
    context_object_name = 'announcements'

    def get_queryset(self, *args, **kwargs):
        return Announcements.objects.filter(type=ANNOUNCEMENT_TYPE_CHOICES[0][0], status=ANNOUNCEMENT_STATUS_CHOICES[0][0])


class DriversList(ListView):
    model = Announcements
    template_name = 'index.html'
    context_object_name = 'announcements'

    def get_queryset(self, *args, **kwargs):
        return Announcements.objects.filter(type=ANNOUNCEMENT_TYPE_CHOICES[1][0], status=ANNOUNCEMENT_STATUS_CHOICES[0][0])


class IndexView(ListView):
    model = Announcements
    template_name = 'index.html'
    context_object_name = 'announcements'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['regions'] = REGION_CHOICES
        return context

    # def get_queryset(self, *args, **kwargs):
    #         return Announcements.objects.filter(user__profile__driver__status='free')

    def change_status(self, *args, **kwargs):
        for announcement in Announcements.objects.all():
            timezone = announcement.departure_time.tzinfo
            # print("Departure", announcement.departure_time)
            time_now = datetime.datetime.now(timezone)
            time_end = time_now + datetime.timedelta(hours=1)
            # print("END", time_end)
            if announcement.departure_time <= time_end:
                # print("Даааа")
                # print(announcement.status)
                announcement.status = ANNOUNCEMENT_STATUS_CHOICES[1][0]
                announcement.save()
                # print(announcement.status)

    def get(self, request, *args, **kwargs):
        self.change_status()
        return super(IndexView, self).get(request, *args, **kwargs)

    def get_queryset(self, *args, **kwargs):
        region = self.request.GET.get('region')
        if region:
            return Announcements.objects.filter(Q(status=ANNOUNCEMENT_STATUS_CHOICES[0][0]), Q(place_from=region) | Q(place_to=region))
        return Announcements.objects.filter(status=ANNOUNCEMENT_STATUS_CHOICES[0][0])


class AnnounceCreateView(LoginRequiredMixin, CreateView):
    form_class = AnnouncementForm
    template_name = 'announce_create.html'
    # form_class = AnnounceCreationForm

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if self.request.user.groups.filter(name="banned").exists():
            raise PermissionDenied("Вы получили бан, доступ к сайту ограничен!")
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(AnnounceCreateView, self).get_context_data(**kwargs)
        try:
            context['form'] = self.form_class(initial={'car': self.request.user.profile.car, 'car_model': self.request.user.profile.car_model})
            return context
        except:
            return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.status = 'active'
        self.object.author = self.request.user
        user = self.request.user
        user.profile.type = form.cleaned_data['type']
        user.profile.car = form.cleaned_data['car']
        user.profile.car_model = form.cleaned_data['car_model']
        print(user.profile.type)
        print(form.cleaned_data['type'], "THIS IS TYPE FORM")
        print(form.cleaned_data['car'], "THIS IS CAR FORM")
        print(form.cleaned_data['car_model'], "THIS IS CAR_MODEL FORM")
        user.profile.save()
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


    # def form_valid(self, form):
    #     self.object = form.save(commit=False)
    #     user = self.request.user
    #     # mobile_phone = form.cleaned_data['mobile_phone']
    #     self.object.departure_time = form.cleaned_data['departure_time']
    #     self.object.seats = form.cleaned_data['seats']
    #     self.object.luggage = form.cleaned_data['luggage']
    #     self.object.place_from = form.cleaned_data['place_from']
    #     self.object.place_to = form.cleaned_data['place_to']
    #     self.object.price = form.cleaned_data['price']
    #     self.object.type = form.cleaned_data['type']
    #     self.object.description = form.cleaned_data['description']
    #     self.object.photo = form.cleaned_data['photo']
    #     self.object.status = 'active'
    #     # if mobile_phone:
    #     #     self.object.mobile_phone = mobile_phone
    #     # else:
    #     #     self.object.phone = self.request.user.profile.phone_number
    #     self.object.author = user
    #     self.object.save()
    #     return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('webapp:index')


class AnnounceDetailView(DetailView):
    model = Announcements
    template_name = 'announce_detail.html'
    context_object_name = 'announce'


class AnnounceUpdateView(LoginRequiredMixin, UpdateView):
    model = Announcements
    template_name = 'change.html'
    fields = ['departure_time', 'seats', 'luggage', 'place_from', 'place_to', 'price', 'type',
            'description', 'photo', 'status']
    context_object_name = 'announce'

    def dispatch(self, request, *args, **kwargs):
        print("Entered")
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if self.request.user.groups.filter(name="banned").exists():
            raise PermissionDenied("Вы получили бан, доступ к сайту ограничен!")
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('webapp:index')


class AnnounceDeleteView(LoginRequiredMixin, DeleteView):
    model = Announcements
    template_name = 'delete.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if self.request.user.groups.filter(name="banned").exists():
            raise PermissionDenied("Вы получили бан, доступ к сайту ограничен!")
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('webapp:index')


class ClientAddView(View):
    def post(self, *args, **kwargs):
        announcement_id = self.request.POST.get('announcement_id')
        quantity = self.request.POST.get('quantity')
        announce = Announcements.objects.get(id=announcement_id)
        user = self.request.user
        if self.request.user.groups.filter(name="banned").exists():
            raise PermissionDenied("Вы получили бан, доступ к сайту ограничен!")
        new = ClientsInAnnounce(announcement=announce, user=user, seats=int(quantity))
        new.save()
        announce.seats -= int(quantity)
        if announce.seats == 0:
            announce.status = 'completed'
        announce.save()
        return redirect('webapp:index')


class ClientDeleteView(View):
    def get(self, *args, **kwargs):
        announce = Announcements.objects.get(id=kwargs['pk'])
        user = announce.clients.get(username=self.request.user)
        clientinannounce = ClientsInAnnounce.objects.get(announcement=announce, user=user)
        announce.seats += clientinannounce.seats
        announce.clients.remove(self.request.user)
        if announce.seats >= 1:
            announce.status = 'active'
        announce.save()
        return redirect('webapp:index')


class ReviewListView(ListView):
    context_object_name = 'reviews'
    model = Review
    ordering = ['-created_at']


class ReviewCreateView(UserPassesTestMixin, CreateView):
    model = Review
    form_class = ReviewForm

    def form_valid(self, form):
        announcement = get_object_or_404(Announcements, pk=self.kwargs.get('pk'))
        review = Review(
            announce=announcement,
            grade=self.request.POST.get('example'),
            text=form.cleaned_data['text'],
            author=self.request.user
        )
        review.save()
        return redirect('accounts:user_detail', pk=review.announce.author_id)

    def test_func(self):
        announcement = get_object_or_404(Announcements, pk=self.kwargs.get('pk'))
        return self.request.user != announcement.author and announcement.status == 'completed'

