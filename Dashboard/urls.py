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
    path('temp/<sample_input>', views.add_course, name = 'temp'),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

