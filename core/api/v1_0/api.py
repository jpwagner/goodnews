import urlparse

from tastypie.api import Api
from tastypie.resources import ModelResource
from tastypie.serializers import Serializer
from tastypie.cache import SimpleCache
from tastypie.throttle import BaseThrottle

from goodnews import models as gn_models


class urlencodeSerializer(Serializer):
    formats = ['json', 'jsonp', 'xml', 'yaml', 'html', 'plist', 'urlencode', 'multipart']
    content_types = {
        'json': 'application/json',
        'jsonp': 'text/javascript',
        'xml': 'application/xml',
        'yaml': 'text/yaml',
        'html': 'text/html',
        'plist': 'application/x-plist',
        'urlencode': 'application/x-www-form-urlencoded',
        'multipart': 'multipart/form-data'
    }

    def from_urlencode(self, data,options=None):
        """ handles basic formencoded url posts """
        qs = dict((k, v if len(v)>1 else v[0] )
            for k, v in urlparse.parse_qs(data).iteritems())
        return qs

    def to_urlencode(self,content): 
        pass

class DummyPaginator(object): 
    def __init__(self, request_data, objects, resource_uri=None,
                 limit=None, offset=0, max_limit=1000,
                 collection_name='objects'):
        self.objects = objects
        self.collection_name = collection_name 

    def page(self):
        return { self.collection_name: self.objects }

class BaseModelResource(ModelResource):
    class Meta:
        allowed_methods = ['get']
        ordering = ['created_date','updated_date']
        exclude_fields = ['created_date','updated_date','is_deleted']
        always_return_data = True
        serializer = urlencodeSerializer()
        cache = SimpleCache(timeout=10)
        throttle = BaseThrottle()
        paginator_class = DummyPaginator

    def determine_format(self, request):
        if (hasattr(request, 'format') and request.format in self._meta.serializer.formats):
            return self._meta.serializer.get_mime_for_format(request.format)
        return 'application/json'        

    def obj_create(self, bundle, **kwargs):
        # override here
        return super(BaseModelResource, self).obj_create(bundle, **kwargs)

    def obj_update(self, bundle, **kwargs):
        # override here
        return super(BaseModelResource, self).obj_update(bundle, **kwargs)

    def dehydrate(self, bundle):
        # Pass in system_fields=1 if you are admin user to show the excluded fields
        system_fields = bundle.request.GET.get('system_fields','')

        if not(system_fields and bundle.request.user.is_staff == True):
            bundle.data = { key : value for key, value in bundle.data.copy().iteritems() if \
                        key not in self.Meta.exclude_fields }
        return bundle

class ArticleResource(BaseModelResource):

    class Meta(BaseModelResource.Meta):
        queryset = gn_models.Article.objects.all()
        resource_name = 'article'

api_resources = Api(api_name='v1.0')
api_resources.register(ArticleResource())
