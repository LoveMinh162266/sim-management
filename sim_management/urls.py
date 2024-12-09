"""
URL configuration for sim_management project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from sim_inventory.views import SimTonKhoViewSet, SimDaBanViewSet
from django.urls import path
from sim_inventory import views  # Import views từ ứng dụng hiện tại

router = DefaultRouter()
router.register(r'sim-ton-kho', SimTonKhoViewSet)
router.register(r'sim-da-ban', SimDaBanViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('admin/', admin.site.urls),
    path('sim/', include('sim_inventory.urls')),  # Gọi URL từ ứng dụng sim_inventory
    # Thêm URL cho giao diện Sim Tồn Kho
    path('sim-ton-kho/', views.sim_ton_kho_view, name='sim_ton_kho'),
    path('sim-da-ban/', views.sim_da_ban_view, name='sim_da_ban'),  # Đảm bảo dòng này có mặt
]