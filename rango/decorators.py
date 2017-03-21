from django.conf import settings
from django.http import HttpResponseRedirect

# Ensures no student can visit another students test results
def correct_student(funct):
    def _check_student(request, student_guid, *args, **kwargs):
        if not request.user.is_staff and request.user.guid() != student_guid:
            return HttpResponseRedirect("{}?next={}".format( settings.LOGIN_URL, request.path))
        return funct(request, student_guid, *args, **kwargs)
    return _check_student
