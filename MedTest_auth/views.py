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
from MedTest_auth.forms import *

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

            session = form.cleaned_data.get('session')
            college = form.cleaned_data.get('college')

            for row in csv_obj:
                objs.append(User(username=row[0], name=row[1], password=make_password(PASSWORD)))

            created_users = User.objects.bulk_create(objs)

            for user in created_users:
                sub_objs.append(StudentProfile(user_id=user, session=session, college=college))
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

class StudentDeleteView(SuccessMessageMixin, DeleteView):
    model = User
    success_message = "Student has been deleted!"

    def get_success_url(self):
        return reverse("auth:manage_student")

class StudentAccountView(CreateView):
    model = User
    template_name = "auth/create_student.html"
    form_class = SingleCreateStudentForm

    def get_success_url(self):
        return reverse("auth:manage_student")

    def form_valid(self, form):
        college = form.cleaned_data.get('college')
        session = form.cleaned_data.get('session')

        form.instance.password = make_password(PASSWORD)
        form = super().form_valid(form)

        messages.success(self.request, f"Account created for {self.object.username}")
        StudentProfile.objects.create(user_id=self.object, session=session, college=college)

        return form

class ManageTest(ListView):
    template_name = 'auth/manage_test.html'

    def get_queryset(self):
        return ScheduleTest.objects.all().order_by('-test_date')

    def get_success_url(self):
        return reverse("auth:manage_test")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = ScheduleTestForm
        return context

    def post(self, request):

        form = ScheduleTestForm(request.POST)

        if form.is_valid():

            session = form.cleaned_data.get('session')
            college = form.cleaned_data.get('college')
            test_date = form.cleaned_data.get('test_date')

            amount = AmountToSchedule.objects.filter().first().amount
            students_list = StudentProfile.objects.filter(session=session, college=college, is_completed=False).order_by('-date_created')[:amount]

            if students_list:

                for student in students_list:
                    ScheduleTest.objects.create(stud_id=student,test_date=test_date)
                    student.save()
                messages.success(self.request, "Medical Test has been scheduled")
            else:
                messages.error(self.request, "Failed in fetching students for the supplied information")
                return render(request, 'auth/manage_test.html',
                context={
                    'form':form,
                    'object_list':self.get_queryset()
                })
        else:
            messages.error(self.request, form.errors.as_text())

            return render(request, 'auth/manage_test.html',
            context={
                'form':form,
                'object_list':self.get_queryset()
            })

        return HttpResponseRedirect(self.get_success_url())

class ScheduleTestView(View):

    def get(self, request):
        form = ScheduleTestForm()
        return render(request, 'auth/schedule_test.html', {'form':form})

class DeleteScheduleView(SuccessMessageMixin, DeleteView):
    model = ScheduleTest
    success_message = "Test has been deleted!"

    def get_success_url(self):
        return reverse("auth:manage_test")

class ViewTest(ListView):
    template_name = 'auth/view_test.html'

    def get_queryset(self):
        stud_id = StudentProfile.objects.get(user_id=self.request.user).stud_id
        return ScheduleTest.objects.filter(stud_id=stud_id).order_by('-test_date')
