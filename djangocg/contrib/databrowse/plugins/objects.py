try:
    from urllib.parse import urljoin
except ImportError:     # Python 2
    from urlparse import urljoin

from django import http
from djangocg.contrib.databrowse.datastructures import EasyModel
from djangocg.contrib.databrowse.sites import DatabrowsePlugin
from djangocg.shortcuts import render_to_response

class ObjectDetailPlugin(DatabrowsePlugin):
    def model_view(self, request, model_databrowse, url):
        # If the object ID wasn't provided, redirect to the model page, which is one level up.
        if url is None:
            return http.HttpResponseRedirect(urljoin(request.path, '../'))
        easy_model = EasyModel(model_databrowse.site, model_databrowse.model)
        obj = easy_model.object_by_pk(url)
        return render_to_response('databrowse/object_detail.html', {'object': obj, 'root_url': model_databrowse.site.root_url})