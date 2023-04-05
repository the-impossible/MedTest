from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.hashers import make_password, check_password
from django.contrib import messages
from django.views import View
import csv, io, codecs
from django.urls import reverse_lazy


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
        return ScheduleTest.objects.filter(result_uploaded=False).order_by('-test_date')

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

class UploadTestResultView(View):

    def get(self, request, stud_id, test_id):
        form = TestResultForm

        student = StudentProfile.objects.get(stud_id=stud_id)

        return render(request, "auth/upload_test.html", context={'form':form, 'student':student, 'type':'Upload'})

    def post(self, request, stud_id, test_id):
        form = TestResultForm(request.POST)
        student = StudentProfile.objects.get(stud_id=stud_id)

        if form.is_valid():
            form = form.save(commit=False)
            form.stud_id = student

            test = ScheduleTest.objects.get(test_id=test_id)
            test.result_uploaded = True
            test.save()

            student.is_completed = True
            student.save()

            form.save()
            messages.success(request, f'Result has been uploaded for {student.user_id.name}')
            return redirect("auth:manage_test")

        else:
            messages.error(request, f'FAILED: {form.errors.as_text()}')

            return render(request, "auth/upload_test.html", context={'form':form, 'student':student, 'type':'Upload'})

class ManageTestResults(ListView):
    template_name = 'auth/manage_results.html'

    def get_queryset(self):
        return TestResult.objects.all().order_by('-date_created')

class UpdateTestResultView(SuccessMessageMixin, UpdateView):
    model = TestResult
    template_name = "auth/upload_test.html"
    form_class = TestResultForm
    success_message = 'Updated Successfully!'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["type"] = 'Update'
        return context

    def get_success_url(self):
        return reverse("auth:manage_results")

class DeleteTestResultView(SuccessMessageMixin, DeleteView):
    model = TestResult
    success_message = 'Updated Successfully!'
    success_url = reverse_lazy('auth:manage_results')

class UpdateProfileView(SuccessMessageMixin, UpdateView):
    model = TestResult
    template_name = "auth/upload_test.html"
    form_class = TestResultForm
    success_message = 'Updated Successfully!'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["type"] = 'Update'
        return context

    def get_success_url(self):
        return reverse("auth:manage_results")

class UpdateProfileView(View):

    studentForm = StudentProfileForm
    picForm = ProfilePicsForm
    passForm = ChangePassForm

    def get(self, request):

        if not request.user.is_staff:
            context = {
                'studentForm':self.studentForm(instance=StudentProfile.objects.get(user_id=request.user.user_id)),

                'picForm':self.picForm,
                'passForm':self.passForm,
            }
        else:
            context = {
                'picForm':self.picForm,
                'passForm':self.passForm,
            }

        return render(request, "auth/update_profile.html", context=context)

    def post(self, request):

        context = {
            'studentForm':self.studentForm,
            'picForm':self.picForm,
            'passForm':self.passForm,
        }

        if 'pass' in request.POST:

            form = self.passForm(request.POST)

            if form.is_valid():
                old_pass = form.cleaned_data.get('old_pass')
                user_pass = request.user.password

                if check_password(old_pass, user_pass):
                    user = User.objects.get(user_id=request.user.user_id)
                    user.password = make_password(form.cleaned_data.get('new_pass'))
                    user.save()
                    messages.success(request, "Password is now updated, you can login to continue!")
                    return redirect("auth:login")
                messages.error(request, "Incorrect current password!")

            messages.error(request, f"{form.errors.as_text()}")
            context["passForm"] = form

        elif 'info' in request.POST:
            student = StudentProfile.objects.get(user_id=request.user.user_id)
            form = self.studentForm(request.POST, instance=student)

            if form.is_valid():
                form.save()
                messages.success(request, f"Profile updated Successfully!")
                return redirect("auth:update_profile")
            else:
                context['studentForm'] = form
                messages.error(request, f"{form.errors.as_text()}")

        elif 'picture' in request.POST:
            user = User.objects.get(user_id=request.user.user_id)
            form = self.picForm(request.POST, request.FILES, instance=user)

            if form.is_valid():
                form.save()
                messages.success(request, f"Profile updated Successfully!")
                return redirect("auth:update_profile")
            else:
                context['picForm'] = form
                messages.error(request, f"{form.errors.as_text()}")

        return render(request, "auth/update_profile.html", context=context)

class ResultView(View):

    def get(self, request, pk):
        try:
            student = StudentProfile.objects.get(user_id=pk)

            if student.age and student.department and student.gender:
                context = {"object": TestResult.objects.get(stud_id=student.stud_id)}
                return render(request, "auth/view_result.html", context)
            if request.user.is_staff:
                messages.error(request, "Student has not updated profile so result cant be viewed")
                return redirect('auth:manage_results')
            messages.error(request, "Update your profile")
            return redirect('auth:update_profile')
        except StudentProfile.DoesNotExist:
            messages.error(request, "Test result has not been uploaded keep checking!")
        except TestResult.DoesNotExist:
            messages.error(request, "Test result has not been uploaded keep checking!")
        return redirect('auth:dashboard')