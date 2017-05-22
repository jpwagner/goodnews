from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin

from . import views

admin.autodiscover()

handler404 = views.my_404_view
handler500 = views.my_500_view

urlpatterns = [

	url(r'^grappelli/', include('grappelli.urls')),
    url(r'^admin/', include(admin.site.urls)),
	url(r'^api/', include('core.api.urls')),
	url(r'^', include('goodnews.urls'))

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)