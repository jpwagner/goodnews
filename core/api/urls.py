from copy import deepcopy

from django.conf import settings
from django.conf.urls import url, include

from .v1_0 import api as v1_0_api

v_latest = deepcopy(v1_0_api.api_resources)
v_latest.api_name = 'latest'

urlpatterns = [

    url(r'^', include(v_latest.urls)),
    url(r'^', include(v1_0_api.api_resources.urls)),

]