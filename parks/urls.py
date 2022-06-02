from django.urls import path
from .views import ParkList, ParkDetail


urlpatterns = [
    path('', ParkList.as_view(), name='park_list'),
    path("<int:pk>/", ParkDetail.as_view(), name='park_detail'),
]