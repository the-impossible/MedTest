from MedTest_auth.models import *

def notification(request):
    if request.user.is_authenticated:
        if not request.user.is_staff:
            stud = StudentProfile.objects.get(user_id=request.user)
            filtered = (x for x in ScheduleTest.objects.filter(stud_id=stud.stud_id).order_by('-test_date') if not x.has_expired )
            all_test = ScheduleTest.objects.filter(stud_id=stud.stud_id).count()
            if stud.age and stud.department and stud.gender:
                profile = True
            profile = False

            return {
                'notify': filtered,
                'completed_test':profile,
                'all_test':all_test,
            }

        else:
            all_test = ScheduleTest.objects.all().count()
            completed_test = StudentProfile.objects.filter(is_completed=True).count()
            incomplete_test = StudentProfile.objects.filter(is_completed=False).count()
            total_student = StudentProfile.objects.filter().count()

            return {
                'all_test':all_test,
                'completed_test':completed_test,
                'incomplete_test':incomplete_test,
                'total_student':total_student,
            }

    return dict()