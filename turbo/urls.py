"""turbo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns

from turbo import settings
from turbo.urlpatterns import api_urlpatterns, conf_urlpatterns

# URL前缀：http://127.0.0.1:8000/zh-hans/
urlpatterns = i18n_patterns(
    path('api/', include(api_urlpatterns)),
)

# URL前缀：http://127.0.0.1:8000/
urlpatterns += [
    path('conf/', include(conf_urlpatterns)),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) \
               + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

