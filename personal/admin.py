from django.contrib import admin

from .models import (
    Faculty,
    Course,
    EmailRecord,
)

# Register your models here.

class FacultyAdmin(admin.ModelAdmin) :
    list_display = ('name', 'email')

    search_fields = ('name', 'email')

    ordering = ('name', 'email')

    filter_horizontal				= ()
    list_filter                     = ()
    fieldsets                       = ()


class CoursesAdmin(admin.ModelAdmin) :
    list_display = ('course_name', 'course_code', 'teacher')
    search_fields = ('course_name', 'course_code', 'teacher')
    ordering = ('course_name', 'course_code', 'teacher')

    # exclude = ('total_feedbacks', 'highest_rate', 'rate_1', 'rate_2', 'rate_3', 'rate_4', 'rate_5')

    filter_horizontal				= ()
    list_filter                     = ()
    fieldsets                       = ()


class EmailRecordAdmin(admin.ModelAdmin) :
    list_display = ('name', 'email', 'enrollment_no')
    search_fields = ('name', 'email', 'enrollment_no')
    ordering = ('name', 'email', 'enrollment_no')

    filter_horizontal				= ()
    list_filter                     = ()
    fieldsets                       = ()


    def delete_model(self, request, obj) -> None:
        print(f"deletes {obj} (email_record)")

        try :
            print(f"deletes {obj.student} (student)")
            
            print(f"deleting {obj.student.user} (user)")
            obj.student.user.delete()

        except Exception as e :
            print("no student exists for email_record")
        
        
        return super().delete_model(request, obj)



admin.site.register(Faculty, FacultyAdmin)
admin.site.register(Course, CoursesAdmin)
admin.site.register(EmailRecord, EmailRecordAdmin)
