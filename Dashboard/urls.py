from django.urls import path
from . import views
from django.views.generic.base import TemplateView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns=[
    path("",views.index,name="dashboard"),
    path("courses/",views.courses,name="courses"),
    path("courses/<str:input_course_name>", views.courses, name="courses_unique"),
    path("course_creation/",views.course_creation,name="course_creation"),
    path("course_access/",views.course_access , name = "course_access"),
    path("courses/announcements/", views.announcements,name="announcements"),
    path('courses/grades', views.grades, name='grades'),
    path('temp/<sample_input>', views.add_course, name = 'temp'),
     path('courses/<str:course_name>/course_email', views.course_email, name="course_email"),
    path('courses/<str:course_name>/assignments',views.assignments,name="assignments"),
    path("courses/<str:course_name>/assignments/assignment_creation", views.assignment_creation, name="assignment_creation"),
    path("courses/<str:course_name>/assignments/<str:name>/assignment_submission/", views.assignment_submission, name="assignment_submission"),
    path("courses/<str:course_name>/assignments/<str:name>/assignment_download/", views.assignment_download, name="assignment_download"),
    path("profile/",views.profile,name="profile"),
    path("settings/",views.edit_profile,name="settings"),
    path("courses/<str:course_name>/assignments/<str:name>/assignment_feedback/",views.assignment_feedback, name = "feedback"),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

