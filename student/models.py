import os


from django.db import models

from django.contrib.auth.models import User


# from course.models import (
#     Assignment,
# )

from personal.models import (
    Course,
    EmailRecord,
)


def custom_upload_to_assignments_submissions(instance, filename) :
    return os.path.join(instance.assignment.course.course_code + '/assignments/submissions/' + instance.student.email_record.enrollment_no + ', ' + filename)

def custom_upload_to_practicals_submissions(instance, filename) :
    return os.path.join(instance.practical.course.course_code + '/practicals/submissions/' + instance.student.email_record.enrollment_no + ', ' + filename)



# Create your models here.

class Student(models.Model) :
    user = models.OneToOneField(User, null=False, on_delete=models.CASCADE)
    # if user is deleted, student is also deleted,

    # name = models.CharField(max_length=255)
    # email = models.EmailField(max_length=255, unique=True)
    # enrollment_no = models.CharField(max_length=255, unique=True)

    email_record = models.OneToOneField(EmailRecord, on_delete=models.CASCADE, default=None)
    # if email_record is deleted, student is also deleted,

    assignments = models.ManyToManyField('course.Assignment', blank=True)
    practicals = models.ManyToManyField('course.Practical', blank=True)


    def __str__(self) :
        return self.email_record.name

class AssignmentSubmission(models.Model) :
    student = models.ForeignKey(Student, null=True, on_delete=models.SET_NULL)
    assignment = models.ForeignKey('course.Assignment', null=True, on_delete=models.SET_NULL)

    answer_file = models.FileField(max_length=255, null=True, upload_to=custom_upload_to_assignments_submissions)

    date = models.DateTimeField(auto_now_add=True, null=True)

    pending = models.BooleanField(default=False)
    submitted = models.BooleanField(default=False)
    late = models.BooleanField(default=False)
    missing = models.BooleanField(default=False)

    def __str__(self) :
        if not self.student or not self.assignment :
            return "student or assignment deleted " + f"id({str(self.id)})"
        return str(self.student.email_record.name) + ', ' + str(self.assignment.assignment_name)

class PracticalSubmission(models.Model) :
    student = models.ForeignKey(Student, null=True, on_delete=models.SET_NULL)
    practical = models.ForeignKey('course.Practical', null=True, on_delete=models.SET_NULL)

    answer_file = models.FileField(max_length=255, null=True, upload_to=custom_upload_to_practicals_submissions)

    date = models.DateTimeField(auto_now_add=True, null=True)


    pending = models.BooleanField(default=False)
    submitted = models.BooleanField(default=False)
    late = models.BooleanField(default=False)
    missing = models.BooleanField(default=False)

    def __str__(self) :
        if not self.student or not self.practical :
            return "student or practical deleted " + f"id({str(self.id)})"
        return str(self.student.email_record.name) + ', ' + str(self.practical.practical_name)


class AttendanceDetails(models.Model) :
    student = models.ForeignKey(Student, null=True, on_delete=models.SET_NULL)
    # this time i used EmailRecord Model to relate AttendanceDetails and a student, rather than Student Model
    # now, we create AttendanceDetails objects when EmailRecord object is created (overriding EmailRecord.save() method)
    
    course = models.ForeignKey(Course, null=True, on_delete=models.SET_NULL)


    total_classes = models.IntegerField(default=0)
    total_presents = models.IntegerField(default=0)
    total_absents = models.IntegerField(default=0)


    def __str__(self) :
        if not self.student or not self.course :
            return "email record or course deleted " + f"id({str(self.id)})"
        return "AttendanceDetails for " + self.student.email_record.enrollment_no + ', ' + str(self.course.course_name)