from django.urls import path
from . import views
from django.views.generic.base import TemplateView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns=[
    path("",views.index,name="dashboard"),
    path("courses/",views.courses,name="courses"),
    path("courses/assignments/",views.assignments,name="assignments"),
    path("profile/",views.profile,name="profile"),
    path("settings/",views.settings,name="settings"),
    path("courses/announcements/", views.announcements,name="announcements"),
    path('courses/grades/', views.grades, name='grades'),
    path('temp/<sample_input>', views.add_course, name = 'temp'),
    path("courses/assignments/assignment_creation", views.assignment_creation, name="assignment_creation"),
    path("courses/assignments/assignment_submission", views.assignment_submission, name="assignment_submission"),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

