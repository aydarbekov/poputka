from django.shortcuts import render
from django.views.generic import ListView, CreateView, DetailView, DeleteView, UpdateView
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse

from webapp.models import Announcements


# class IndexView(ListView):
#     model = Announcements
#     template_name = 'index.html'
#     context_object_name = 'announcements'

    # def get_queryset(self, *args, **kwargs):
    #         return Announcements.objects.filter(user__profile__driver__status='free')


# class AnnounceCreateView(CreateView):
#     model = Ad
#     template_name = 'announce_create.html'
#     # form_class = AnnounceCreationForm
#     fields = ['direction', 'time', 'seats', 'luggage', 'place_from', 'place_to', 'car_number', 'car', 'price']

    # def get_form_kwargs(self):
    #     print(self.request.user)
    #     kwargs = super().get_form_kwargs()
    #     kwargs['author'] = self.request.user
    #     return kwargs

    # def form_valid(self, form):
    #     self.object = form.save(commit=False)
    #     user = self.request.user
    #     # mobile_phone = form.cleaned_data['mobile_phone']
    #     self.object.direction = form.cleaned_data['direction']
    #     self.object.time = form.cleaned_data['time']
    #     self.object.seats = form.cleaned_data['seats']
    #     self.object.luggage = form.cleaned_data['luggage']
    #     self.object.place_from = form.cleaned_data['place_from']
    #     self.object.place_to = form.cleaned_data['place_to']
    #     self.object.car_number = form.cleaned_data['car_number']
    #     self.object.car = form.cleaned_data['car']
    #     self.object.price = form.cleaned_data['price']
    #     # if mobile_phone:
    #     #     self.object.mobile_phone = mobile_phone
    #     # else:
    #     #     self.object.phone = self.request.user.profile.phone_number
    #     self.object.user_id = user.pk
    #     self.object.save()
    #     return HttpResponseRedirect(self.get_success_url())
    #
    # def get_success_url(self):
    #     return reverse('webapp:index')


# class AnnounceDetailView(DeleteView):
#     model = Ad
#     template_name = 'announce_detail.html'
#     context_object_name = 'announce'
#
#
# class AnnounceUpdateView(UpdateView):
#     model = Ad
#     template_name = 'change.html'
#     fields = ['direction', 'time', 'seats', 'luggage', 'place_from', 'place_to', 'car_number', 'car', 'price']
#     context_object_name = 'announce'
#
#     def get_success_url(self):
#         return reverse('webapp:index')
#
#
# class AnnounceDeleteView(DeleteView):
#     model = Ad
#     template_name = 'delete.html'
#
#     def get_success_url(self):
#         return reverse('webapp:index')
