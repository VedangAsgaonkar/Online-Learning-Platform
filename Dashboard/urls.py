from django.urls import path
from . import views
from django.views.generic.base import TemplateView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns=[
    path("",views.index,name="dashboard"),
    path("courses/",views.courses,name="courses"),
    path("assignments/",views.assignments,name="assignments"),
    path("courses/announcements/", views.announcements,name="announcements"),
    path('courses/grades/', views.grades, name='grades'),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# path('', TemplateView.as_view(template_name='dashboard.html'), name='dashboard'),
#     path('courses/', TemplateView.as_view(template_name='courses.html'), name='courses'),
#     path('assignments/', TemplateView.as_view(template_name='assignments.html'), name='assignments'),
#     path('courses/announcements/', TemplateView.as_view(template_name='announcements.html'), name='announcements'),
#     path('courses/grades/', TemplateView.as_view(template_name='grades.html'), name='grades'),