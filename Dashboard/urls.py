from os import name
from django.urls import path, re_path, include
from . import views
from django.views.generic.base import TemplateView
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_jwt.views import refresh_jwt_token

urlpatterns=[
    path("",views.index,name="dashboard"),
    path("courses/",views.courses,name="courses"),
    path("courses/<str:input_course_name>", views.courses, name="courses_unique"),
    path("courses/<str:course_name>/participants/", views.participants, name="participants"),
    path("course_creation/",views.course_creation,name="course_creation"),
    path("course_access/",views.course_access , name = "course_access"),
    path("courses/<str:course_name>/announcements/", views.announcements,name="announcements"),
    path("courses/<str:course_name>/announcements/stop/", views.stop_announcements,name="stop_announcements"),
    path("courses/<str:course_name>/announcements/resume/", views.start_announcements,name="start_announcements"),
    path("courses/<str:course_name>/announcements/create/", views.announcements_create,name="announcements_create"),
    path("courses/<str:course_name>/announcements/<str:id>/reply/", views.announcements_reply,name="announcements_reply"),
    path('courses/<str:course_name>/grades', views.grades, name='grades'),
    path('temp/<sample_input>', views.add_course, name = 'temp'),
    path('courses/<str:course_name>/course_stats', views.course_stats, name='course_stats'),
    path('courses/<str:course_name>/course_email', views.course_email, name="course_email"),
    path('courses/<str:course_name>/assignments',views.assignments,name="assignments"),
    path("courses/<str:course_name>/assignments/assignment_creation", views.assignment_creation, name="assignment_creation"),
    path("courses/<str:course_name>/assignments/content_creation", views.content_creation, name="content_creation"),
    path("courses/<str:course_name>/assignments/<str:name>/assignment_submission/", views.assignment_submission, name="assignment_submission"),
    path("courses/<str:course_name>/assignments/<str:name>/assignment_download/", views.assignment_download, name="assignment_download"),
    path("courses/<str:course_name>/assignments/<str:name>/content_view/", views.content_view, name="content_view"),
    path("profile/",views.profile,name="profile")   ,
    path("settings/",views.edit_profile,name="settings"),
    path("messages/", views.message_list, name="message_list"),
    path("messages/<str:person>/", views.chat_screen,name="chat_screen"),
    path("courses/<str:course_name>/assignments/<str:name>/edit_properties/edit_deadline/",views.edit_deadline, name = "edit_deadline"),
    path("courses/<str:course_name>/assignments/<str:name>/assignment_feedback/",views.assignment_feedback, name = "feedback"),
    path("courses/<str:course_name>/assignments/<str:name>/<str:student_name>/",views.GUI_grader, name = "GUI_grader"),
    re_path(r'^rest-auth/', include('rest_auth.urls')),
    re_path(r'^rest-auth/registration/', include('rest_auth.registration.urls')),
    re_path(r'^refresh-token/', refresh_jwt_token),
    path('rest/courses/', views.rest_courses, name='rest_courses'),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

