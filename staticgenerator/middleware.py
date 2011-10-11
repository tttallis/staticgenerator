import re
from django.conf import settings
from staticgenerator import StaticGenerator

class StaticGeneratorMiddleware(object):
    """
    This requires settings.STATIC_GENERATOR_URLS tuple to match on URLs
    
    Example::
        
        STATIC_GENERATOR_URLS = (
            r'^/$',
            r'^/blog',
        )
        
    """
    urls = tuple([re.compile(url) for url in settings.STATIC_GENERATOR_URLS])
    gen = StaticGenerator()
    
    def process_response(self, request, response):
        path = request.path_info
        query_string = request.META.get('QUERY_STRING', '')
        if response.status_code == 200 and not request.user.is_authenticated():
            if request.POST: # if request contains a post, we don't write to cache
                return response
            for url in self.urls:
                if url.match(path):
                    self.gen.publish_from_path(path, query_string, response.content)
                    break
        return response
