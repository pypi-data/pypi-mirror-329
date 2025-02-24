from django.contrib import admin
from django.urls import path
from django.urls import path,re_path,include
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
import debug_toolbar
from.url_base import get_url_patterns as get_url_patterns_base
from.url_spartaqube import get_url_patterns as get_url_patterns_spartaqube
handler404='project.sparta_1f3dab4412.sparta_24bc9093ce.qube_78b5f17039.sparta_eb2fb9818c'
handler500='project.sparta_1f3dab4412.sparta_24bc9093ce.qube_78b5f17039.sparta_888ab5ef1e'
handler403='project.sparta_1f3dab4412.sparta_24bc9093ce.qube_78b5f17039.sparta_dc132243b1'
handler400='project.sparta_1f3dab4412.sparta_24bc9093ce.qube_78b5f17039.sparta_9daf73dbd7'
urlpatterns=get_url_patterns_base()+get_url_patterns_spartaqube()
if settings.B_TOOLBAR:urlpatterns+=[path('__debug__/',include(debug_toolbar.urls))]