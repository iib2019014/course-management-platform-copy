from django.urls import path


from .views import (
    renderCourseDetailsView,
    renderCourseMaterialsView,
    renderAssignmentView,
    renderPracticalView,
    renderAttendanceView,
    renderAttendanceDetailsView,
    renderAssignmentSubmitView,
    renderPracticalSubmitView,
    renderFeedbacksView,
    renderFeedbackSubmitView,
    renderAnnouncementsView,
    renderCourseUpdatesView,
)


urlpatterns = [
    path('<str:course_id>/details', renderCourseDetailsView, name='details'),
    
    
    path('<str:course_id>/materials', renderCourseMaterialsView, name='materials'),
    # rather than course/materials/1 can we use course/1/materials ????
    path('<str:course_id>/assignments', renderAssignmentView, name='assignments'),
    path('<str:course_id>/practicals', renderPracticalView, name='practicals'),
    path('<str:course_id>/attendance', renderAttendanceView, name='attendance'),
    path('<str:course_id>/feedbacks', renderFeedbacksView, name='feedbacks'),
    path('<str:course_id>/announcements', renderAnnouncementsView, name='announcements'),
    path('<str:course_id>/course-updates', renderCourseUpdatesView, name='course-updates'),
    
    path('attendance-details/<str:attendance_id>', renderAttendanceDetailsView, name='attendance-details'),
    
    
    path('submit-assignment/<str:assignment_id>', renderAssignmentSubmitView, name='submit-assignment'),
    path('submit-practical/<str:practical_id>', renderPracticalSubmitView, name='submit-practical'),
    path('<str:course_id>submit-feedback', renderFeedbackSubmitView, name='submit-feedback'),
]