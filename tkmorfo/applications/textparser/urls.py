from django.conf.urls import url
from .views import ParserView

urlpatterns = [
	url(r'^analisis/parser/',ParserView.as_view(),name='analysis'),
]
