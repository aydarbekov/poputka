from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView
from accounts.forms import SignUpForm, ProfileFormset


class SignUp(CreateView):
    form_class = SignUpForm
    template_name = 'user_create.html'
    success_url = reverse_lazy('accounts:login')

    def get_context_data(self, **kwargs):
        form_type = self.request.GET.get('form')
        if 'formset' not in kwargs:
            kwargs['formset'] = ProfileFormset()
        return super().get_context_data(**kwargs)

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        formset = ProfileFormset(data=request.POST)

        if form.is_valid() and formset.is_valid():
            return self.form_valid_for_full(form, formset)
        return self.form_invalid_for_full(form, formset)

    def form_valid_for_full(self, form, formset):
        self.object = form.save(commit=True)
        self.object.save()
        formset.instance = self.object
        formset.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid_for_full(self, form, formset):
        return self.render_to_response(self.get_context_data(form=form, formset=formset))



class UserDetailView(DetailView):
    model = User
    template_name = 'user_detail.html'
    context_object_name = 'user_obj'

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     # context['form'] = TaskForm()
    #     files = context['user_obj'].file.order_by('-creation_date')
    #
    #     # print(files.objects.filter(type='general'))
    #     # print(files)
    #     self.paginate_files_to_context(files, context)
    #     return context
    #
    # def paginate_files_to_context(self, files, context):
    #     paginator = Paginator(files, 3, 0)
    #     page_number = self.request.GET.get('page', 1)
    #     page = paginator.get_page(page_number)
    #     context['paginator'] = paginator
    #     context['page_obj'] = page
    #     context['files'] = page.object_list
    #     context['is_paginated'] = page.has_other_pages()

