from django.contrib import admin
from django.urls import path
from django.urls import path,re_path,include
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
import debug_toolbar
from.url_base import get_url_patterns as get_url_patterns_base
from.url_spartaqube import get_url_patterns as get_url_patterns_spartaqube
handler404='project.sparta_4040e628cb.sparta_1225405abb.qube_5988036840.sparta_aaaf02d987'
handler500='project.sparta_4040e628cb.sparta_1225405abb.qube_5988036840.sparta_6621f6d12f'
handler403='project.sparta_4040e628cb.sparta_1225405abb.qube_5988036840.sparta_96b4caccbf'
handler400='project.sparta_4040e628cb.sparta_1225405abb.qube_5988036840.sparta_aa324bd552'
urlpatterns=get_url_patterns_base()+get_url_patterns_spartaqube()
if settings.B_TOOLBAR:urlpatterns+=[path('__debug__/',include(debug_toolbar.urls))]