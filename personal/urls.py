from django.urls import path


from .views import (
    renderHomeView,
    renderCourseListView,
)


urlpatterns = [
    path('', renderHomeView, name='home'),
    path('courses/<str:faculty_id>', renderCourseListView, name='course-list'),
]