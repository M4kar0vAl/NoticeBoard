from django.urls import path
from .views import *

urlpatterns = [
    path('adverts/', AdvertList.as_view(), name='advert_list'),
    path('user_adverts', AdvertList.as_view(), name='user_advert_list'),
    path('adverts/<int:pk>', AdvertDetail.as_view(), name='advert_detail'),
    path('adverts/create', AdvertCreate.as_view(), name='advert_create'),
    path('adverts/<int:pk>/edit', AdvertEdit.as_view(), name='advert_edit'),
    path('adverts/<int:pk>/delete', AdvertDelete.as_view(), name='advert_delete'),
    path('response/create', ResponseCreate.as_view(), name='response_create'),
    path('responses/', ResponseList.as_view(), name='response_list'),
    path('responses/user', ResponseList.as_view(), name='user_response_list'),
    path('responses/<int:pk>', ResponseDetail.as_view(), name='response_detail'),
    path('responses/<int:pk>/edit', ResponseEdit.as_view(), name='response_edit'),
    path('responses/<int:pk>/delete', ResponseDelete.as_view(), name='response_delete'),
    path('responses/action_handle', response_action_handle, name='response_handle'),
    path('subscriptions/', subscriptions, name='subscriptions')
]