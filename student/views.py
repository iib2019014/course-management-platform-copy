from django.shortcuts import redirect, render

from django.contrib.auth import (
    authenticate,
    login,
    logout,
)

from .models import (
    AttendanceDetails,
    Student,
)


from personal.models import (
    EmailRecord,
)

from student.models import (
    AssignmentSubmission,
    PracticalSubmission,
)

from .forms import (
    UserRegistrationForm,
)


APP_NAME = 'student'

# Create your views here.


def renderLoginView(request) :
    if(request.user.is_authenticated) :
        return redirect('home')


    context = {}

    if request.method == 'POST' :
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None :
            login(request, user)

            print('logged in')

            return redirect('home')
        else :
            print("incorrect username or password")
            return redirect('login')
    else :
        return render(request, APP_NAME + '/login.html', context)

def renderRegisterView(request) :
    if(request.user.is_authenticated) :
        return redirect('home')

    context = {}
    
    if request.method == 'POST' :
        registerForm = UserRegistrationForm(request.POST)
        
        if registerForm.is_valid() :
            enrollment_no=request.POST['enrollment_no']

            # check if the enrollment_no is there or not,
            try :
                email_record = EmailRecord.objects.get(enrollment_no__iexact=enrollment_no)

            
            except EmailRecord.DoesNotExist :
                print("EmailRecord does not exist")
                return redirect('home')
            
            
            
            # check if an account is already registered for that enrollment_no
            try :
                students = Student.objects.get(email_record=email_record)
                print("student already registered")
                return redirect('home')
            
            except Student.DoesNotExist :
                print("student not registered")

                

            user = registerForm.save()

            student = Student.objects.create(
                user=user,

                # name and email must be retrieved from the college record of that enrollment_no,
                # name=email_record.name,
                # email=email_record.email,

                # enrollment_no=enrollment_no,
                
                email_record=email_record,
            )

            print(f"student for {student} created")


            # when a new student is registered,
                # we will create submission objects for practicals and assignments that are already posted for his courses,

            enrolled_courses = email_record.enrolled_courses.all()
            for course in enrolled_courses :
                course_practicals = course.practical_set.all()
                for practical in course_practicals :
                    practical_submission = PracticalSubmission.objects.create(
                        student=student,
                        practical=practical,
                    )

                course_assignments = course.assignment_set.all()
                for assignment in course_assignments :
                    assignment_submission = AssignmentSubmission.objects.create(
                        student=student,
                        assignment=assignment,
                    )

                
                attendance_details = AttendanceDetails.objects.create(
                    student=student,
                    course=course,
                )

            print(f"student --> {student}")

            return redirect('login')
        else :
            context['registerForm'] = registerForm
            print(f"RegisterForm Invalid")
    else :
        registerForm = UserRegistrationForm()
        context['registerForm'] = registerForm
        # print(registerForm)

    return render(request, APP_NAME + '/register.html', context)


def renderLogoutView(request) :
    if request.user.is_authenticated :
        logout(request)
    return redirect('home')