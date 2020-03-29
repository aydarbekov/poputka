from django.shortcuts import render
from django.views.generic import ListView, CreateView, DetailView, DeleteView, UpdateView
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from webapp.models import Announcements, ANNOUNCEMENT_TYPE_CHOICES, REGION_CHOICES


class PassengersList(ListView):
    model = Announcements
    template_name = 'index.html'
    context_object_name = 'announcements'

    def get_queryset(self, *args, **kwargs):
        return Announcements.objects.filter(type=ANNOUNCEMENT_TYPE_CHOICES[0][0])


class DriversList(ListView):
    model = Announcements
    template_name = 'index.html'
    context_object_name = 'announcements'

    def get_queryset(self, *args, **kwargs):
        print(Announcements.objects.all())
        print(Announcements.objects.filter(type=ANNOUNCEMENT_TYPE_CHOICES[0][0]))
        print(Announcements.objects.filter(type=ANNOUNCEMENT_TYPE_CHOICES[1][0]))
        return Announcements.objects.filter(type=ANNOUNCEMENT_TYPE_CHOICES[1][0])


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
