from django.db import models
from decimal import Decimal

class SimTonKho(models.Model):
    so_thu_tu = models.AutoField(primary_key=True, default=1)
    so_thue_bao = models.CharField(max_length=15, unique=True)
    gia_thu_goc = models.DecimalField(max_digits=10, decimal_places=0)
    gia_chiet_khau = models.DecimalField(max_digits=10, decimal_places=0)
    nha_mang = models.CharField(max_length=50)
    trang_thai = models.CharField(
        max_length=10,
        choices=[('Còn', 'Còn'), ('Đã bán', 'Đã bán')],
        default='Còn'
    )
    ngay_ban = models.DateField(null=True, blank=True)
    nguoi_ban = models.CharField(max_length=100, null=True, blank=True)
    phi_giao_dich = models.DecimalField(max_digits=10, decimal_places=0, null=True, blank=True)  # Đổi sang DecimalField

    def __str__(self):
        return self.so_thue_bao

class SimDaBan(models.Model):
    so_thu_tu = models.AutoField(primary_key=True, default=1)
    so_thue_bao = models.CharField(max_length=15, unique=True)
    gia_thu_goc = models.DecimalField(max_digits=10, decimal_places=0)
    gia_chiet_khau = models.DecimalField(max_digits=10, decimal_places=0)
    phi_giao_dich = models.DecimalField(max_digits=10, decimal_places=0)
    thuc_thu = models.DecimalField(max_digits=10, decimal_places=0, null=True, blank=True)
    ngay_ban = models.DateField()
    nguoi_ban = models.CharField(max_length=50)
    nha_mang = models.CharField(max_length=50)

    def save(self, *args, **kwargs):
        self.thuc_thu = self.gia_chiet_khau - self.phi_giao_dich
        super().save(*args, **kwargs)

    def __str__(self):
        return self.so_thue_bao