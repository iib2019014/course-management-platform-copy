from django.db import models

# from student.models import (
    # AttendanceDetails,
# )

# Create your models here.
class Faculty(models.Model) :
    name = models.CharField(max_length=255, null=False)
    email = models.EmailField(max_length=255, unique=True)

    # courses = models.one


    def __str__(self) :
        return self.name


class Course(models.Model) :
    course_name = models.CharField(max_length=255, null=False)
    course_code = models.CharField(max_length=255, null=False)

    teacher = models.ForeignKey(Faculty, null=True, on_delete=models.SET_NULL)


    total_feedbacks = models.IntegerField(default=0)
    highest_rate = models.IntegerField(default=0)

    rate_5 = models.IntegerField(default=0)
    rate_4 = models.IntegerField(default=0)
    rate_3 = models.IntegerField(default=0)
    rate_2 = models.IntegerField(default=0)
    rate_1 = models.IntegerField(default=0)


    def __str__(self) :
        return self.course_name


class EmailRecord(models.Model) :
    name = models.CharField(max_length=255, null=False)
    email = models.EmailField(max_length=255, null=False, unique=True)
    enrollment_no = models.CharField(max_length=255, null=False, unique=True)
    
    enrolled_courses = models.ManyToManyField(Course, blank=True)
    # I kept this field in EmailRecord because this will be done by the college administration,
    
    def __str__(self) :
        return f"EmailRecord {self.name} ({self.email})"


    # def save(self, *args, **kwargs) :

    #     super().save(*args, **kwargs)

    #     courses = self.enrolled_courses.all()
    #     print(f"courses = {courses}")
    #     print(f"enrollment_no {self.enrollment_no}")

    #     for course in courses :
    #         print(f"creating AttendanceDetails object for {self.enrollment_no}, {course.course_name}")

    #         attendance_details = 'personal.AttendanceDetails'.objects.create(
    #             email_record=self,
    #             course=course,
    #         )

        # super().save(*args, **kwargs)
        