import pkg_resources
from channels.routing import ProtocolTypeRouter,URLRouter
from django.urls import re_path as url
from django.conf import settings
from project.sparta_8da3d59761.sparta_ce9238fa69 import qube_fe62767934,qube_90c06e1ebd,qube_171fc244cf,qube_eb00f38140,qube_ca997984ec,qube_a5c0d24019,qube_e051ca5457,qube_e9f5031b30,qube_0aa0b4ac71
from channels.auth import AuthMiddlewareStack
import channels
channels_ver=pkg_resources.get_distribution('channels').version
channels_major=int(channels_ver.split('.')[0])
print('CHANNELS VERSION')
print(channels_ver)
def sparta_86d4233c9a(this_class):
	A=this_class
	if channels_major<=2:return A
	else:return A.as_asgi()
urlpatterns=[url('ws/statusWS',sparta_86d4233c9a(qube_fe62767934.StatusWS)),url('ws/notebookWS',sparta_86d4233c9a(qube_90c06e1ebd.NotebookWS)),url('ws/wssConnectorWS',sparta_86d4233c9a(qube_171fc244cf.WssConnectorWS)),url('ws/pipInstallWS',sparta_86d4233c9a(qube_eb00f38140.PipInstallWS)),url('ws/gitNotebookWS',sparta_86d4233c9a(qube_ca997984ec.GitNotebookWS)),url('ws/xtermGitWS',sparta_86d4233c9a(qube_a5c0d24019.XtermGitWS)),url('ws/hotReloadLivePreviewWS',sparta_86d4233c9a(qube_e051ca5457.HotReloadLivePreviewWS)),url('ws/apiWebserviceWS',sparta_86d4233c9a(qube_e9f5031b30.ApiWebserviceWS)),url('ws/apiWebsocketWS',sparta_86d4233c9a(qube_0aa0b4ac71.ApiWebsocketWS))]
application=ProtocolTypeRouter({'websocket':AuthMiddlewareStack(URLRouter(urlpatterns))})
for thisUrlPattern in urlpatterns:
	try:
		if len(settings.DAPHNE_PREFIX)>0:thisUrlPattern.pattern._regex='^'+settings.DAPHNE_PREFIX+'/'+thisUrlPattern.pattern._regex
	except Exception as e:print(e)