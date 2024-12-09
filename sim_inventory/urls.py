from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SimTonKhoViewSet, SimDaBanViewSet, sim_ton_kho_view, sim_da_ban_view

router = DefaultRouter()
router.register(r'sim-ton-kho', SimTonKhoViewSet)
router.register(r'sim-da-ban', SimDaBanViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('sim-ton-kho/', sim_ton_kho_view, name='sim_ton_kho_view'),
    path('sim-da-ban/', sim_da_ban_view, name='sim_da_ban_view'),
]