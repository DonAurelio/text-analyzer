from django.conf.urls import url
from .views import IndexView

urlpatterns = [
    url(r'^index/process',IndexView.as_view(),name='index'),
]