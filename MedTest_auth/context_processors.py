from MedTest_auth.models import *

def notification(request):
    if request.user.is_authenticated:
        if not request.user.is_staff:
            stud_id = StudentProfile.objects.get(user_id=request.user).stud_id
            filtered = (x for x in ScheduleTest.objects.filter(stud_id=stud_id).order_by('-test_date') if not x.has_expired )
            return {'notify': filtered}

    return dict()