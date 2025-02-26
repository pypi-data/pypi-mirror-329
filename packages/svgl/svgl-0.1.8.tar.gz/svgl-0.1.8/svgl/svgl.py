# -*- coding: utf-8 -*-

import httpx
import pathlib

from .settings import Settings

class SVGLResource:

    def __init__(self, settings):
        self._settings = settings
        
    def __getattr__(self, item):
        if item.startswith("_"):
            raise AttributeError(item)
    
        _settings = self._settings.copy()
        
        if item == "library":
            _settings.base_url = self._settings.base_url.replace("api", "library")
            return SVGLResource(_settings)
        elif item == "output":
            _settings.output = 1
            return SVGLResource(_settings)
        
        if _settings.base_url.endswith("/"):
            _settings.base_url = self._settings.base_url + item  
        elif _settings.type_logo:
            _settings.color = item
        elif "search" in _settings.base_url:
            _settings.type_logo = item
        elif "?" in _settings.base_url:
            _settings.base_url = self._settings.base_url + "&" + item
        elif not _settings.base_url.endswith("/"):
            _settings.base_url = self._settings.base_url + "?" + item

        return SVGLResource(_settings)
    
    def __call__(self, resource=None):
        if resource in (None, ""):
            return self
        
        _settings = self._settings.copy()
        
        if _settings.base_url.endswith("library/"):
            _settings.base_url = self._settings.base_url + str(resource) + "." + _settings.extention
        elif _settings.output == 1:
            _settings.output = pathlib.Path(resource)
        else:
            _settings.base_url = self._settings.base_url + "=" + str(resource)

        return SVGLResource(_settings)

    def _request(self, method, url, **kwargs):
        response = httpx.request(method, url, **kwargs)
        try:
            return response.json()
        except:
            return response

    def get(self, **kwargs):
        return self._request("GET", self._settings.base_url, **kwargs)
    
    def post(self, **kwargs):
        return self._request("POST", self._settings.base_url, **kwargs)
    
    def put(self, **kwargs):
        return self._request("PUT", self._settings.base_url, **kwargs)
    
    def delete(self, **kwargs):
        return self._request("DELETE", self._settings.base_url, **kwargs)
    
    def patch(self, **kwargs):
        return self._request("PATCH", self._settings.base_url, **kwargs)
    
    def options(self, **kwargs):
        return self._request("OPTIONS", self._settings.base_url, **kwargs)
    
    def head(self, **kwargs):
        return self._request("HEAD", self._settings.base_url, **kwargs)
    
    def trace(self, **kwargs):
        return self._request("TRACE", self._settings.base_url, **kwargs)
    
    def connect(self, **kwargs):
        return self._request("CONNECT", self._settings.base_url, **kwargs)
    
    def download(self, **kwargs):
        response = self._request("GET", self._settings.base_url, **kwargs)
        if response.status_code == 200:
            try:
                if self._settings.color:
                    response = self._request("GET", response.json()[0][self._settings.type_logo][self._settings.color], **kwargs)
                else:
                    response = self._request("GET", response.json()[0][self._settings.type_logo], **kwargs)
            except AttributeError:
                pass
            filename = str(response.url).split("/")[-1]
            open(self._settings.output / filename, 'wb').write(response.content)
        return response

class SVGL(SVGLResource):
    
    def __init__(self):
        self._settings = Settings()
        super().__init__(self._settings)