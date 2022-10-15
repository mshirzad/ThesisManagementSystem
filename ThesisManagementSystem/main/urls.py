from django.urls import path, include

from rest_framework.routers import DefaultRouter

from main import views


router = DefaultRouter()

router.register('records', views.getRecords, basename='records')
router.register('add', views.addRecord, basename='add')



app_name = 'main'

urlpatterns = [
    path('', include(router.urls))
]