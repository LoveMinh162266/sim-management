from rest_framework import viewsets
from .models import SimTonKho, SimDaBan
from .serializers import SimTonKhoSerializer, SimDaBanSerializer
from django.shortcuts import redirect, render, get_object_or_404
from django.http import JsonResponse
from django.core.paginator import Paginator
from rest_framework.pagination import PageNumberPagination
from datetime import datetime
from django.db.models import Sum
from sim_inventory import models
import logging

logger = logging.getLogger(__name__)

class SimTonKhoPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100

# API ViewSet cho Sim tồn kho
class SimTonKhoViewSet(viewsets.ModelViewSet):
    queryset = SimTonKho.objects.all()
    serializer_class = SimTonKhoSerializer
    pagination_class = SimTonKhoPagination

# API ViewSet cho Sim đã bán
class SimDaBanViewSet(viewsets.ModelViewSet):
    queryset = SimDaBan.objects.all()
    serializer_class = SimDaBanSerializer

# View hiển thị danh sách Sim tồn kho
def sim_ton_kho_view(request):
    so_thue_bao = request.GET.get('so_thue_bao', None)
    if so_thue_bao:
        sim_ton_kho_list = SimTonKho.objects.filter(so_thue_bao__icontains=so_thue_bao).order_by('so_thu_tu')
    else:
        sim_ton_kho_list = SimTonKho.objects.order_by('so_thu_tu')
    paginator = Paginator(sim_ton_kho_list, 100)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    return render(request, 'sim_ton_kho.html', {'page_obj': page_obj})

# View hiển thị danh sách Sim đã bán với tổng doanh thu
def sim_da_ban_view(request):
    sim_list = SimDaBan.objects.all().order_by('so_thu_tu')
    paginator = Paginator(sim_list, 100)  # Hiển thị 100 SIM mỗi trang
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    total_chiet_khau = sim_list.aggregate(total=Sum('gia_chiet_khau'))['total'] or 0
    total_thuc_thu = sim_list.aggregate(total=Sum('thuc_thu'))['total'] or 0

    context = {
        'page_obj': page_obj,
        'total_chiet_khau': total_chiet_khau,
        'total_thuc_thu': total_thuc_thu,
    }
    return render(request, 'sim_da_ban.html', context)

