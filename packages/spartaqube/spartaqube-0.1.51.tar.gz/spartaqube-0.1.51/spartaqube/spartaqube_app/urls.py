from django.contrib import admin
from django.urls import path
from django.urls import path,re_path,include
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
import debug_toolbar
from.url_base import get_url_patterns as get_url_patterns_base
from.url_spartaqube import get_url_patterns as get_url_patterns_spartaqube
handler404='project.sparta_1f6c7513e9.sparta_6a04a4059f.qube_0701ea60e4.sparta_80c743a678'
handler500='project.sparta_1f6c7513e9.sparta_6a04a4059f.qube_0701ea60e4.sparta_d7cc234f2f'
handler403='project.sparta_1f6c7513e9.sparta_6a04a4059f.qube_0701ea60e4.sparta_7021ad208b'
handler400='project.sparta_1f6c7513e9.sparta_6a04a4059f.qube_0701ea60e4.sparta_03722c66ac'
urlpatterns=get_url_patterns_base()+get_url_patterns_spartaqube()
if settings.B_TOOLBAR:urlpatterns+=[path('__debug__/',include(debug_toolbar.urls))]