from MedTest_auth.models import *

def notification(request):
    if not request.user.is_staff:
        stud_id = StudentProfile.objects.get(user_id=request.user).stud_id
        return {'notify': ScheduleTest.objects.filter(stud_id=stud_id).order_by('-test_date')[0]}
    return dict()
