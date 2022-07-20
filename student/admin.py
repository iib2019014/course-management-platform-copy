from django.contrib import admin

from .models import (
    Student,
    AssignmentSubmission,
    PracticalSubmission,
    AttendanceDetails,
)


class StudentAdmin(admin.ModelAdmin) :
    def delete_model(self, request, obj) -> None:
        print(f"deletes {obj}")
        
        print(f"deleting {obj.user}")
        obj.user.delete()

        return super().delete_model(request, obj)


# Register your models here.
admin.site.register(Student, StudentAdmin)
admin.site.register(AssignmentSubmission)
admin.site.register(PracticalSubmission)
admin.site.register(AttendanceDetails)