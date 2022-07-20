from django.contrib import admin

from .models import (
    CourseMaterial,
    Assignment,
    Practical,
    DailyAttendance,
    Feedback,
    Question,
    FeedbackQAndA,
    Announcement,
    CourseUpdate,
)

# Register your models here.


admin.site.register(CourseMaterial)
admin.site.register(Assignment)
admin.site.register(Practical)
admin.site.register(DailyAttendance)
admin.site.register(Feedback)
admin.site.register(Question)
admin.site.register(FeedbackQAndA)
admin.site.register(Announcement)
admin.site.register(CourseUpdate)