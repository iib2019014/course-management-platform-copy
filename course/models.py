import datetime
import os
import pandas as pd

from django.db import models
from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

from django.utils import timezone


from personal.models import (
    Course,
    EmailRecord,
    Faculty,
)

from student.models import (
    AttendanceDetails,
    Student,
    AssignmentSubmission,
    PracticalSubmission,
)

# Create your models here.

MATERIAL_TYPE = (
    ('Link', 'Link'),
    ('File', 'File'),
)

ASSIGNMENT_TYPE = (
    ('Theory', 'Theory'),
    ('Lab', 'Lab'),
)

PRACTICAL_TYPE = (
    ('Offline', 'Offline'),
    ('Online', 'Online'),
)

RATING = (
    (1, 1),
    (2, 2),
    (3, 3),
    (4, 4),
    (5, 5),
)

REMARK = (
    ('Excellent', 'Excellent'),
    ('Very Good', 'Very Good'),
    ('Good', 'Good'),
    ('Fair', 'Fair'),
    ('Poor', 'Poor'),
    ('Very Poor', 'Very Poor'),
)



def custom_upload_to_materials(instance, filename) :
    return os.path.join(instance.course.course_code + '/materials/' + filename)

def custom_upload_to_assignments(instance, filename) :
    return os.path.join(instance.course.course_code + '/assignments/' + filename)

def custom_upload_to_practicals(instance, filename) :
    return os.path.join(instance.course.course_code + '/practicals/' + filename)

def custom_upload_to_attendance(instance, filename) :
    return os.path.join(instance.course.course_code + '/attendance/' + filename)



class CourseMaterial(models.Model) :
    material_name = models.CharField(max_length=255, blank=False)
    
    material_type = models.CharField(max_length=255, null=False, choices=MATERIAL_TYPE)

    material_link = models.CharField(max_length=255, blank=True)

    material_file = models.FileField(max_length=255, blank=True, upload_to=custom_upload_to_materials)

    course = models.ForeignKey(Course, null=True, on_delete=models.SET_NULL)


    def __str__(self) :
        return 'material for ' + self.course.course_name + ' (' + str(self.id) +')'

    def save(self, *args, **kwargs) :
        try :
            instructor = self.course.teacher.name
        except Exception as e :
            instructor = None
        course = self.course.course_name

        # students = Student.objects.all()

        email_records = self.course.emailrecord_set.all()
        for email_record in email_records :
            print("trying ", email_record)
            try :
                if email_record.student :
                    name = email_record.name

                    email_body = render_to_string('course/material_mail.html', {'name': name, 'instructor': instructor, 'course': course})
                    recipient = email_record.email

                    email = EmailMessage(
                        'New Material',
                        email_body,
                        settings.EMAIL_HOST_USER,
                        [recipient],
                    )

                    email.send()

                    print(f"mail sent to {email_record.email}")
            except Student.DoesNotExist :
                print("student is not registered")

            super().save(*args, **kwargs)


class Assignment(models.Model) :
    assignment_name = models.CharField(max_length=255, blank=False)

    assignment_type = models.CharField(max_length=255, null=False, choices=ASSIGNMENT_TYPE)

    questions_link = models.CharField(max_length=255, blank=True)

    questions_file = models.FileField(max_length=255, blank=True, upload_to=custom_upload_to_assignments)

    course = models.ForeignKey(Course, null=True, on_delete=models.SET_NULL)
    
    deadline = models.DateTimeField(blank=False)

    def __str__(self) :
        return 'assignment for ' + self.course.course_name + ' (' + str(self.id) + ')'


    def save(self, *args, **kwargs) :
        try :
            instructor = self.course.teacher.name
        except Exception as e :
            instructor = None
        course = self.course.course_name

        super().save(*args, **kwargs)

        # students = Student.objects.all()

        email_records = self.course.emailrecord_set.all()
        for email_record in email_records :
            print("trying ", email_record)
            try :
                if email_record.student :
                    # first create an AssignmentSubmission object,
                    assignment_submission = AssignmentSubmission.objects.create(
                        student=email_record.student,
                        assignment=self,
                    )

                    name = email_record.name

                    email_body = render_to_string('course/assignment_mail.html', {'name': name, 'instructor': instructor, 'course': course})
                    recipient = email_record.email

                    email = EmailMessage(
                        'New Assignment',
                        email_body,
                        settings.EMAIL_HOST_USER,
                        [recipient],
                    )

                    email.send()

                    print(f"mail sent to {email_record.email}")
            except Student.DoesNotExist :
                print("student is not registered")

        # super().save(*args, **kwargs)


class Practical(models.Model) :
    practical_name = models.CharField(max_length=255, blank=False)

    practical_type = models.CharField(max_length=255, null=False, choices=PRACTICAL_TYPE)

    questions_link = models.CharField(max_length=255, blank=True)

    questions_file = models.FileField(max_length=255, blank=True, upload_to=custom_upload_to_practicals)

    lab_room_no = models.CharField(max_length=255, blank=True)

    instructor = models.ForeignKey(Faculty, null=True, on_delete=models.SET_NULL)

    time = models.DateTimeField(blank=False)

    course = models.ForeignKey(Course, null=True, on_delete=models.SET_NULL)

    def __str__(self) :
        return 'practical for ' + self.course.course_name + ' (' + str(self.id) + ')'


    def save(self, *args, **kwargs) :
        try :
            instructor = self.instructor.name
        except Exception as e :
            instructor = None
        course = self.course.course_name

        super().save(*args, **kwargs)


        # students = Student.objects.all()

        # email_records enrolled in this course,
        email_records = self.course.emailrecord_set.all()
        for email_record in email_records :
            print("trying ", email_record)
            try :
                if email_record.student :
                    # student = email_record.student

                    practical_submission = PracticalSubmission.objects.create(
                        student=email_record.student,
                        practical=self,
                    )

                    name = email_record.name

                    email_body = render_to_string('course/practical_email.html', {'name': name, 'instructor': instructor, 'course': course})
                    recipient = email_record.email

                    email = EmailMessage(
                        'New Practical',
                        email_body,
                        settings.EMAIL_HOST_USER,
                        [recipient],
                    )

                    email.send()
                    
                    print(f"mail sent to {email_record.email}")
            except Student.DoesNotExist :
                print("student is not registered")



class DailyAttendance(models.Model) :
    attendance_sheet = models.FileField(max_length=255, upload_to=custom_upload_to_attendance)

    date = models.DateTimeField(blank=False, auto_now_add=True)

    course = models.ForeignKey(Course, null=True, on_delete=models.SET_NULL)

    def __str__(self) :
        if not self.course :
            return f"course is deleted, id({self.id})"
        return 'attendance for ' + self.course.course_name + ' (' + str(self.date) + ')'


    def save(self, *args, **kwargs) :

        super().save(*args, **kwargs)

        file_path = settings.MEDIA_ROOT + '/' + self.attendance_sheet.name

        attendance_df = pd.read_excel(file_path)

        print(attendance_df.head())
        print(f"columns {attendance_df.columns}")

        enrollment_numbers = attendance_df['Enrollment Number']
        attendance = attendance_df['Attendance']

        for enrollment_number, present  in zip(enrollment_numbers, attendance) :
            print(f"for {enrollment_number}")
            try :
                email_record = EmailRecord.objects.get(enrollment_no__iexact=enrollment_number)

                try :
                    student = Student.objects.get(email_record=email_record)

                    try :
                        attendance_details = AttendanceDetails.objects.get(student=student, course=self.course)

                        attendance_details.total_classes += 1

                        if present.lower() == 'yes' :
                            attendance_details.total_presents += 1

                        if present.lower() == 'no' :
                            attendance_details.total_absents += 1

                        attendance_details.save()

                    except AttendanceDetails.DoesNotExist :
                        print("AttendanceDetails object does not exist")

                except Student.DoesNotExist :
                    print('Student does not exist')

            except EmailRecord.DoesNotExist :
                print('Email record does not exist')



class Question(models.Model) :
    question = models.CharField(max_length=255, blank=False)

    def __str__(self) :
        return self.question




class Feedback(models.Model) :
    student = models.ForeignKey(Student, null=True, on_delete=models.SET_NULL)
    course = models.ForeignKey(Course, null=True, on_delete=models.SET_NULL)

    rate = models.IntegerField(null=False, choices=RATING)
    review = models.TextField(blank=True)

    def __str__(self) :
        if not self.student or not self.course :
            return "student or course deleted " + f"id({str(self.id)})"
        return 'by ' + self.student.email_record.name + ' to ' + self.course.course_name + f"({self.id})"


class FeedbackQAndA(models.Model) :
    question = models.CharField(max_length=255, blank=False)
    answer = models.CharField(max_length=255, blank=True)

    feedback = models.ForeignKey(Feedback, null=True, on_delete=models.SET_NULL)

    def __str__(self) :
        if not self.feedback :
            return f"feedback deleted id ({self.id})"
        return f"Q and A for feedback {self.feedback.id}"



class Announcement(models.Model) :
    content = models.TextField(blank=False)

    course = models.ForeignKey(Course, null=True, on_delete=models.SET_NULL)

    date = models.DateTimeField(default=timezone.now)

    def __str__(self) :
        if not self.course :
            return "course deleted " + f"id({str(self.id)})"
        return f"for {self.course.course_name}, {self.id}"



class CourseUpdate(models.Model) :
    content = models.TextField(blank=True)

    course = models.ForeignKey(Course, null=True, on_delete=models.SET_NULL)

    link = models.CharField(max_length=255, blank=True)

    date = models.DateTimeField(default=timezone.now)

    def __str__(self) :
        if not self.course :
            return "course deleted " + f"id({str(self.id)})"
        return f"update {self.id} for {self.course.course_code}"