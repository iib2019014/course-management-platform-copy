from django.shortcuts import render

from .models import (
    Faculty,
    Course,
)

APP_NAME = 'personal'

# Create your views here.



def renderHomeView(request) :
    # if(request.user.is_authenticated) :
    #     courses = request.user.student.email_record.enrolled_courses.all()
    #     print(courses)

    #     for course in courses :
    #         emailrecord_set = course.emailrecord_set.all()
    #         print(course, emailrecord_set)
    
    context = {}

    facultys = Faculty.objects.all()
    context['facultys'] = facultys

    return render(request, APP_NAME + '/home.html', context)


def renderCourseListView(request, faculty_id) :
    context = {}

    faculty = Faculty.objects.filter(id=faculty_id).first()

    if request.user.is_authenticated :
        if not request.user.is_superuser :
            email_record = request.user.student.email_record

            student_courses = email_record.enrolled_courses.all().filter(teacher=faculty)
            context['student_courses'] = student_courses

    else :
        faculty_courses = faculty.course_set.all()
        context['faculty_courses'] = faculty_courses

    return render(request, APP_NAME + '/course_list.html', context)