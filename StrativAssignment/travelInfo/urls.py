from django.urls import path
from .views import DistrictListCreateView, GetAvgForecast, TravelDecision

urlpatterns = [
    path('district/', DistrictListCreateView.as_view(), name='district-list-create'),
    path('getForecast/', GetAvgForecast.as_view(), name='getForecast-list-create'),
    path('travel-decision/', TravelDecision.as_view(), name='travel-decision'),
]
