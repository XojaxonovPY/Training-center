from django.urls import path

from apps.views import ImageGenericApiView

urlpatterns = [
    path('image/url',ImageGenericApiView.as_view()),
]