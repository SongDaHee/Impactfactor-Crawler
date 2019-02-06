from django.urls import path
from django.conf.urls import url
#from django.views.generic import RedirectView

from . import views

urlpatterns = [
	#path('', views.index, name='index'),
	#path('test', views.DisplayProfessor, name='test'),
	#url(r'test', views.DisplayProfessor, name='DisplayProfessor'),
	url('test/(?P<professorId>.+)', views.DisplayProfessor,name='DisplayProfessor'),
	url('base', views.DisplayBase,name='DisplayBase'),
	#url('searcbTest', RedirectView.as_view(pattern_name='DisplayBase', permanent=False)),
]