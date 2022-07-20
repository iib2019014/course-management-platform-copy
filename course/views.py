# import datetime
import os
import pandas as pd
from django.utils import timezone

from django.conf import settings

from django.shortcuts import render, redirect
from django.template.defaulttags import register

from django.contrib.auth.decorators import login_required
from django.contrib import messages

from personal.models import (
    Faculty,
    Course,
)

from course.models import (
    Assignment,
    CourseUpdate,
    Practical,
    DailyAttendance,
    Feedback,
    Question,
    FeedbackQAndA,
    Announcement,
)

from student.models import (
    AssignmentSubmission,
    AttendanceDetails,
    PracticalSubmission,
)


from .forms import (
    AssignmentSubmissionForm,
    PracticalSubmissionForm,
    FeedbackForm,
)

APP_NAME = 'course'

# Create your views here.


def renderCourseDetailsView(request, course_id) :
    context = {}

    course = Course.objects.filter(id=course_id).first()

    context["course"] = course

    return render(request, APP_NAME + '/materials.html', context)


def renderCourseMaterialsView(request, course_id) :

    context = {}

    course = Course.objects.filter(id=course_id).first()

    course_materials = course.coursematerial_set.all()


    # since I was not passing course in to context to materials.html template I got the error,
        # NoReverseMatch at /course/materials/4
        # Reverse for 'materials' with arguments '('',)' not found. 1 pattern(s) tried: ['course/materials/(?P<course_id>[^/]+)\\Z']

        # course.id is used in materials.html template
        
    context["course"] = course

    context["course_materials"] = course_materials

    # print(f"course_materials = {course_materials}")

    return render(request, APP_NAME + '/materials.html', context)

@register.filter
def isAssignmentMissing(request, assignment_id) :
    assignment = Assignment.objects.filter(id=assignment_id).first()

    print(f"{assignment.deadline}, {timezone.now()}")

    return assignment.deadline < timezone.now()


def renderAssignmentView(request, course_id) :

    context = {}


    course = Course.objects.filter(id=course_id).first()
    context["course"] = course


    course_assignments = course.assignment_set.all()

    if request.user.is_authenticated :
        student = request.user.student
        print(f"{student} logged in")

        submitted, late, pending, missing = [], [], [], []
        for course_assignment in course_assignments :
            assignment_submission = AssignmentSubmission.objects.filter(student=student, assignment=course_assignment).first()
            try :
                submitted.append(assignment_submission.submitted)
                late.append(assignment_submission.late)
                pending.append(assignment_submission.pending)
                missing.append(assignment_submission.missing)
            except Exception as e :
                messages.info(request, "There are assignments posted before you registered yourself")
                print(f"assignment_submission is None for {student}")

            # print(f"{course_assignment}, {assignment_submission}, {assignment_submission.submitted}")

        context['assignment_submissions'] = zip(course_assignments, late, submitted, missing, pending)


    else :
        print("not logged in")
        context["course_assignments"] = course_assignments

    return render(request, APP_NAME + '/assignments.html', context)


@login_required(login_url='login')
def renderAssignmentSubmitView(request, assignment_id) :
    context = {}
    
    assignment = Assignment.objects.filter(id=assignment_id).first()
    course = assignment.course
    context["course"] = course


    if request.method == 'POST' :
        assignmentSubmissionForm = AssignmentSubmissionForm(request.POST, request.FILES)
        if assignmentSubmissionForm.is_valid() :

            file = request.FILES['answer_file']


            # get the AssignmentSubmission object corresponding to this student and assignment,
            student = request.user.student
            assignment_submission = AssignmentSubmission.objects.filter(student=student, assignment=assignment).first()
            if assignment_submission.submitted :
                print(f"already submitted")
            else :
                print(f"not submitted")
            
            print("updating file")
            assignment_submission.answer_file = file

            assignment_submission.submitted = True
            assignment_submission.pending = False
            assignment_submission.missing = False
            # get the deadline and if it is passed, then set late to True
            if assignment.deadline < timezone.now() :
                assignment_submission.late = True


            print("saving")
            assignment_submission.save()

            return redirect('assignments', course.id)
        else :
            print(assignmentSubmissionForm.errors)
            print("assignment submission form is invalid")

    else :
        assignmentSubmissionForm = AssignmentSubmissionForm()
        # print(assignmentSubmissionForm)
        context['assignmentSubmissionForm'] = assignmentSubmissionForm

    return render(request, APP_NAME + '/assignment_submit.html', context)



def renderPracticalView(request, course_id) :

    context = {}

    course = Course.objects.filter(id=course_id).first()

    course_practicals = course.practical_set.all()


        
    context["course"] = course

    if request.user.is_authenticated :
        student = request.user.student
        
        submitted = []
        for course_practical in course_practicals :
            practical_submission = PracticalSubmission.objects.filter(student=student, practical=course_practical).first()
            try :
                submitted.append(practical_submission.submitted)
            except Exception as e :
                messages.info(request, "There are practicals posted before you registered yourself")
                print(f"practical_submission is None for {student}")

        context['practical_submissions'] = zip(course_practicals, submitted)

    else :
        context["course_practicals"] = course_practicals

    # print(f"course_practicals = {course_practicals}")

    return render(request, APP_NAME + '/practicals.html', context)


@login_required(login_url='login')
def renderPracticalSubmitView(request, practical_id) :
    context = {}

    practical = Practical.objects.filter(id=practical_id).first()

    course = practical.course
    context["course"] = course


    if request.method == 'POST' :
        practicalSubmissionForm = PracticalSubmissionForm(request.POST, request.FILES)

        file = request.FILES['file']

        student = request.user.student

        practical_submission = PracticalSubmission.objects.filter(student=student, practical=practical).first()
        

        practical_submission.answer_file = file

        practical_submission.submitted = True
        practical_submission.pending = False
        
        practical_submission.save()

        return redirect('practicals', course.id)

    else :
        practicalSubmissionForm = PracticalSubmissionForm()
        context['practicalSubmissionForm'] = practicalSubmissionForm

    return render(request, APP_NAME + '/practical_submit.html', context)



# @login_required(login_url='login')
def renderAttendanceView(request, course_id) :

    context = {}

    course = Course.objects.filter(id=course_id).first()

    course_attendances = course.dailyattendance_set.all()


        
    context["course"] = course

    # attendance_tables = {}

    # for course_attendance in course_attendances :
    #     print(f"name is {course_attendance.attendance_sheet.name}")
    #     attendance_tables[str(course_attendance.date)] = pd.read_excel(settings.MEDIA_ROOT + '/' + course_attendance.attendance_sheet.name)
    #     print(f"type {type(attendance_tables[str(course_attendance.date)])}")
    #     print(attendance_tables[str(course_attendance.date)])

    # context["attendance_tables"] = attendance_tables
    context["course_attendances"] = course_attendances

    # print(f"course_attendances = {course_attendances}")


    # if user is logged in, get the attendance_details for the student in this course,
    if request.user.is_authenticated :
        
        student = request.user.student
        
        attendance_details = AttendanceDetails.objects.filter(student=student, course=course).first()

        context['total_classes'] = attendance_details.total_classes
        context['total_presents'] = attendance_details.total_presents
        context['total_absents'] = attendance_details.total_absents

    return render(request, APP_NAME + '/attendances.html', context)


# @login_required(login_url='login')
def renderAttendanceDetailsView(request, attendance_id) :

    context = {}

    attendance = DailyAttendance.objects.filter(id=attendance_id).first()

    context['course'] = attendance.course

    file_path = settings.MEDIA_ROOT + '/' + attendance.attendance_sheet.name

    attendance_df = pd.read_excel(file_path)

    # print(f"index {attendance_df.index}")
    # print(f"columns {attendance_df.columns}")
    # print(f"dtypes {attendance_df.dtypes}")
    # print(attendance_df.shape)
    # print(attendance_df.head)

    # print(list(attendance_df['Name']))

    columns = list(attendance_df.columns)
    context['columns'] = columns

    attendance_table = zip(range(len(attendance_df['Name'])), list(attendance_df['Name']), list(attendance_df['Enrollment Number']), list(attendance_df['Attendance']))

    context['attendance_table'] = attendance_table


    return render(request, APP_NAME + '/attendance_details.html', context)


def renderFeedbacksView(request, course_id) :
    context = {}

    course = Course.objects.filter(id=course_id).first()
    context['course'] = course
    
    course_feedbacks = course.feedback_set.all()
    context['course_feedbacks'] = course_feedbacks


    context['total_feedbacks'] = course.total_feedbacks
    context['highest_rate'] = course.highest_rate
    context['rate_5'] = course.rate_5
    context['rate_4'] = course.rate_4
    context['rate_3'] = course.rate_3
    context['rate_2'] = course.rate_2
    context['rate_1'] = course.rate_1


    return render(request, APP_NAME + '/feedbacks.html', context)


@login_required(login_url='login')
def renderFeedbackSubmitView(request, course_id) :
    context = {}

    questions = Question.objects.all()
    context['questions'] = questions

    course = Course.objects.filter(id=course_id).first()
    context['course'] = course

    if request.method == 'POST' :
        feedbackForm = FeedbackForm(request.POST)
        if feedbackForm.is_valid() :
            # print(request.POST)
            rate = int(request.POST['how_would_you_rate_the_course'])
            
            feedback = Feedback.objects.create(
                student=request.user.student,
                course=course,
                rate=rate,
                review=request.POST['review']
            )

            course.total_feedbacks += 1
            if rate > course.highest_rate :
                course.highest_rate = rate
            if rate == 5 :
                course.rate_5 += 1
            if rate == 4 :
                course.rate_4 += 1
            if rate == 3 :
                course.rate_3 += 1
            if rate == 2 :
                course.rate_2 += 1
            if rate == 1 :
                course.rate_1 += 1

            course.save()


            questions = Question.objects.all()
            print(f"questions {questions}")

            answers = request.POST.getlist('answers')
            
            for question, answer in zip(questions, answers) :
                feedback_qanda = FeedbackQAndA.objects.create(
                    question=question,
                    answer=answer,
                    feedback=feedback,
                )





            print(f"Feedback {feedback}")

            return redirect('feedbacks', course_id)
        
        else :
            print('Feedback form is invalid')
            print(feedbackForm.errors)
            context['feedbackForm'] = feedbackForm

    else :
        feedbackForm = FeedbackForm()
        # print(feedbackForm)
        context['feedbackForm'] = feedbackForm

    return render(request, APP_NAME + '/feedback_submit.html', context)


def renderAnnouncementsView(request, course_id) :
    context = {}

    course = Course.objects.filter(id=course_id).first()

    context['course'] = course

    announcements = Announcement.objects.filter(course=course)

    context['announcements'] = announcements


    return render(request, APP_NAME + '/announcements.html', context)


def renderCourseUpdatesView(request, course_id) :
    context = {}

    course = Course.objects.filter(id=course_id).first()

    context['course'] = course

    course_updates = CourseUpdate.objects.filter(course=course)

    context['course_updates'] = course_updates


    return render(request, APP_NAME + '/updates.html', context)