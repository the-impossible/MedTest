from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.views import View
import csv, io, codecs


from MedTest_auth.models import *
from MedTest_auth.forms import CreateStudentForm

PASSWORD = '12345678'
# Create your views here.

class DashboardView(TemplateView):
    template_name = "auth/dashboard.html"

class LoginView(View):
    def get(self, request):
        return render(request, 'auth/login.html')

    def post(self, request):
        username = request.POST.get('username').upper().strip()
        password = request.POST.get('password').strip()

        if username and password:
            user = authenticate(request, username=username, password=password)

            if user:
                if user.is_active:
                    login(request, user)
                    messages.success(request, f"You are now signed in {user}")

                    nxt  = request.GET.get('next', None)
                    if nxt is None:
                        return redirect('auth:dashboard')
                    return redirect(self.request.GET.get('next', None))

                else:
                    messages.warning(request, 'Account not active contact the administrator')
            else:
                messages.error(request, 'Invalid login credentials')
        else:
            messages.error(request, 'All fields are required!!')

        return redirect('auth:login')

class LogoutView(LoginRequiredMixin, View):

    def post(self, request):
        logout(request)
        messages.success(request, 'You are successfully logged out, to continue login again')
        return redirect('auth:login')

class ManageStudentAccount(ListView):
    template_name = 'auth/manage_student.html'
    def get_queryset(self):
        return StudentProfile.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = CreateStudentForm
        return context

    def post(self, request):

        form = CreateStudentForm(request.POST, request.FILES)

        if form.is_valid():

            csv_obj = csv.reader(codecs.iterdecode(request.FILES['file'], 'utf-8'))

            objs = []
            sub_objs = []

            programme = form.cleaned_data.get('programme')
            session = form.cleaned_data.get('session')
            college = form.cleaned_data.get('college')

            for row in csv_obj:
                objs.append(User(username=row[0], name=row[1], password=make_password(PASSWORD)))

            created_users = User.objects.bulk_create(objs)

            for user in created_users:
                sub_objs.append(StudentProfile(user_id=user, programme=programme, session=session, college=college))
            created_user_profiles = StudentProfile.objects.bulk_create(sub_objs)

        else:
            messages.error(self.request, form.errors.as_text())

            return render(request, 'auth/manage_student.html',
            context={
                'form':form,
                'object_list':self.get_queryset()
            })

        return HttpResponseRedirect(self.get_success_url())


    def get_success_url(self):
        return reverse("auth:manage_student")








