from django.urls import path
from .views import RounteView, CreateRouteView, UpdateRouteView


urlpatterns = [
    path('allRoutes',RounteView.as_view()),
    path('createRoute',CreateRouteView.as_view()),
    path('updateRoute',UpdateRouteView.as_view()),
]
