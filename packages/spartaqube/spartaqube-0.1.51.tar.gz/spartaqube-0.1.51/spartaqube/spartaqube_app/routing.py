import pkg_resources
from channels.routing import ProtocolTypeRouter,URLRouter
from django.urls import re_path as url
from django.conf import settings
from project.sparta_3c031cc253.sparta_810178638e import qube_3fd888790b,qube_19f9b74b8a,qube_81c8b2dc12,qube_0e0653db97,qube_1556013317,qube_d04bc5c12b,qube_767670af59,qube_93eb217da2,qube_e89bf8a938
from channels.auth import AuthMiddlewareStack
import channels
channels_ver=pkg_resources.get_distribution('channels').version
channels_major=int(channels_ver.split('.')[0])
print('CHANNELS VERSION')
print(channels_ver)
def sparta_6c9da308fc(this_class):
	A=this_class
	if channels_major<=2:return A
	else:return A.as_asgi()
urlpatterns=[url('ws/statusWS',sparta_6c9da308fc(qube_3fd888790b.StatusWS)),url('ws/notebookWS',sparta_6c9da308fc(qube_19f9b74b8a.NotebookWS)),url('ws/wssConnectorWS',sparta_6c9da308fc(qube_81c8b2dc12.WssConnectorWS)),url('ws/pipInstallWS',sparta_6c9da308fc(qube_0e0653db97.PipInstallWS)),url('ws/gitNotebookWS',sparta_6c9da308fc(qube_1556013317.GitNotebookWS)),url('ws/xtermGitWS',sparta_6c9da308fc(qube_d04bc5c12b.XtermGitWS)),url('ws/hotReloadLivePreviewWS',sparta_6c9da308fc(qube_767670af59.HotReloadLivePreviewWS)),url('ws/apiWebserviceWS',sparta_6c9da308fc(qube_93eb217da2.ApiWebserviceWS)),url('ws/apiWebsocketWS',sparta_6c9da308fc(qube_e89bf8a938.ApiWebsocketWS))]
application=ProtocolTypeRouter({'websocket':AuthMiddlewareStack(URLRouter(urlpatterns))})
for thisUrlPattern in urlpatterns:
	try:
		if len(settings.DAPHNE_PREFIX)>0:thisUrlPattern.pattern._regex='^'+settings.DAPHNE_PREFIX+'/'+thisUrlPattern.pattern._regex
	except Exception as e:print(e)