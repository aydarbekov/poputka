from datetime import datetime, timedelta
from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, DetailView, DeleteView, UpdateView
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.views.generic.base import View

from webapp.models import Announcements, ANNOUNCEMENT_TYPE_CHOICES, ANNOUNCEMENT_STATUS_CHOICES


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

    def change_status(self, *args, **kwargs):
        for announcement in Announcements.objects.all():
            timezone = announcement.departure_time.tzinfo
            # print("Departure", announcement.departure_time)
            time_now = datetime.now(timezone)
            time_end = time_now + timedelta(hours=1)
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
        return Announcements.objects.filter(status=ANNOUNCEMENT_STATUS_CHOICES[0][0])


class AnnounceCreateView(CreateView):
    model = Announcements
    template_name = 'announce_create.html'
    # form_class = AnnounceCreationForm
    fields = ['departure_time', 'seats', 'luggage', 'place_from', 'place_to', 'price', 'type',
            'description', 'photo', 'status']
    # clients = models.ManyToManyField('auth.User', null=True, blank=True, related_name='clients',
    #                                  verbose_name='Клиенты')

    # def get_form_kwargs(self):
    #     print(self.request.user)
    #     kwargs = super().get_form_kwargs()
    #     kwargs['author'] = self.request.user
    #     return kwargs

    def form_valid(self, form):
        self.object = form.save(commit=False)
        user = self.request.user
        # mobile_phone = form.cleaned_data['mobile_phone']
        self.object.departure_time = form.cleaned_data['departure_time']
        self.object.seats = form.cleaned_data['seats']
        self.object.luggage = form.cleaned_data['luggage']
        self.object.place_from = form.cleaned_data['place_from']
        self.object.place_to = form.cleaned_data['place_to']
        self.object.price = form.cleaned_data['price']
        self.object.type = form.cleaned_data['type']
        self.object.description = form.cleaned_data['description']
        self.object.photo = form.cleaned_data['photo']
        self.object.status = form.cleaned_data['status']
        # if mobile_phone:
        #     self.object.mobile_phone = mobile_phone
        # else:
        #     self.object.phone = self.request.user.profile.phone_number
        self.object.author = user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('webapp:index')


class AnnounceDetailView(DeleteView):
    model = Announcements
    template_name = 'announce_detail.html'
    context_object_name = 'announce'
#
#
class AnnounceUpdateView(UpdateView):
    model = Announcements
    template_name = 'change.html'
    fields = ['departure_time', 'seats', 'luggage', 'place_from', 'place_to', 'price', 'type',
            'description', 'photo', 'status']
    context_object_name = 'announce'

    def get_success_url(self):
        return reverse('webapp:index')


class AnnounceDeleteView(DeleteView):
    model = Announcements
    template_name = 'delete.html'

    def get_success_url(self):
        return reverse('webapp:index')


class ClientAddView(View):
    def get(self, *args, **kwargs):
        Announce = Announcements.objects.get(id=kwargs['pk'])
        Announce.clients.add(self.request.user)
        Announce.seats -= 1
        Announce.save()
        return redirect('webapp:index')

class ClientDeleteView(View):
    def get(self, *args, **kwargs):
        Announce = Announcements.objects.get(id=kwargs['pk'])
        Announce.clients.remove(self.request.user)
        Announce.seats += 1
        Announce.save()
        return redirect('webapp:index')