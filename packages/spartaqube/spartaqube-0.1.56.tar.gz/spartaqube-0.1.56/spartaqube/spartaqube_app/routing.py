import pkg_resources
from channels.routing import ProtocolTypeRouter,URLRouter
from django.urls import re_path as url
from django.conf import settings
from project.sparta_3500f2f8a8.sparta_4ef991e0ba import qube_1f7eccdb78,qube_a3e4df9700,qube_47582773c6,qube_2e6cc9e756,qube_a2642e6fd7,qube_0c590dc781,qube_614294318f,qube_9acd24caae,qube_b7a0a00aa1
from channels.auth import AuthMiddlewareStack
import channels
channels_ver=pkg_resources.get_distribution('channels').version
channels_major=int(channels_ver.split('.')[0])
print('CHANNELS VERSION')
print(channels_ver)
def sparta_800a19129d(this_class):
	A=this_class
	if channels_major<=2:return A
	else:return A.as_asgi()
urlpatterns=[url('ws/statusWS',sparta_800a19129d(qube_1f7eccdb78.StatusWS)),url('ws/notebookWS',sparta_800a19129d(qube_a3e4df9700.NotebookWS)),url('ws/wssConnectorWS',sparta_800a19129d(qube_47582773c6.WssConnectorWS)),url('ws/pipInstallWS',sparta_800a19129d(qube_2e6cc9e756.PipInstallWS)),url('ws/gitNotebookWS',sparta_800a19129d(qube_a2642e6fd7.GitNotebookWS)),url('ws/xtermGitWS',sparta_800a19129d(qube_0c590dc781.XtermGitWS)),url('ws/hotReloadLivePreviewWS',sparta_800a19129d(qube_614294318f.HotReloadLivePreviewWS)),url('ws/apiWebserviceWS',sparta_800a19129d(qube_9acd24caae.ApiWebserviceWS)),url('ws/apiWebsocketWS',sparta_800a19129d(qube_b7a0a00aa1.ApiWebsocketWS))]
application=ProtocolTypeRouter({'websocket':AuthMiddlewareStack(URLRouter(urlpatterns))})
for thisUrlPattern in urlpatterns:
	try:
		if len(settings.DAPHNE_PREFIX)>0:thisUrlPattern.pattern._regex='^'+settings.DAPHNE_PREFIX+'/'+thisUrlPattern.pattern._regex
	except Exception as e:print(e)