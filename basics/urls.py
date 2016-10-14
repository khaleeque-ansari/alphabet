__author__ = 'khaleeque'
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^index.html', views.index, name='index'),
    url(r'^resume.html', views.resume, name='resume'),
    url(r'^resume.pdf', views.resume_pdf, name='resume_pdf'),

]
