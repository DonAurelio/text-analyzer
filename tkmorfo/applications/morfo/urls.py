from django.conf.urls import url
from .views import MorfoView

urlpatterns = [
	url(r'^',MorfoView.as_view(),name='analysis'),
]
