from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from import_export import resources
from .models import SimTonKho, SimDaBan
from django.contrib.humanize.templatetags.humanize import intcomma

# Resource cho SimTonKho
class SimTonKhoResource(resources.ModelResource):
    class Meta:
        model = SimTonKho
        import_id_fields = ('so_thu_tu',)  # Trường dùng để nhận diện khi nhập/xuất
        fields = ('so_thu_tu', 'so_thue_bao', 'gia_thu_goc', 'gia_chiet_khau', 'nha_mang')  # Các trường được xử lý
def skip_row(self, instance, original, row, import_validation_errors=None):
        # Bỏ qua dòng nếu bất kỳ trường nào bị thiếu dữ liệu
        if not row.get('gia_thu_goc') or not row.get('so_thue_bao'):
            return True
        return super().skip_row(instance, original, row, import_validation_errors)

# Resource cho SimDaBan
class SimDaBanResource(resources.ModelResource):
    class Meta:
        model = SimDaBan
        import_id_fields = ('so_thu_tu',)
        fields = ('so_thu_tu', 'so_thue_bao', 'gia_thu_goc', 'gia_chiet_khau', 
                  'phi_giao_dich', 'thuc_thu', 'ngay_ban', 'nguoi_ban', 'nha_mang')
def skip_row(self, instance, original, row, import_validation_errors=None):
        # Bỏ qua dòng nếu bất kỳ trường nào bị thiếu dữ liệu
        if not row.get('gia_thu_goc') or not row.get('so_thue_bao'):
            return True
        return super().skip_row(instance, original, row, import_validation_errors)

# Admin cho SimTonKho
class SimTonKhoAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = SimTonKhoResource
    list_display = ('so_thu_tu', 'so_thue_bao', 'formatted_gia_thu_goc', 'formatted_gia_chiet_khau', 'nha_mang', 'trang_thai')
    search_fields = ('so_thue_bao', 'gia_thu_goc', 'gia_chiet_khau', 'nha_mang')
    list_filter = ('trang_thai', 'nha_mang')
    actions = ['chuyen_sang_da_ban']
    
    def chuyen_sang_da_ban(self, request, queryset):
        """
        Chuyển các SIM được chọn sang trạng thái 'Đã bán' và thêm vào SimDaBan.
        """
        count = 0
        errors = []
        for sim in queryset:
            if sim.trang_thai != 'Còn':
                errors.append(f"SIM {sim.so_thue_bao} không ở trạng thái 'Còn'.")
                continue

            if not sim.ngay_ban or not sim.nguoi_ban or not sim.phi_giao_dich:
                errors.append(f"SIM {sim.so_thue_bao} thiếu dữ liệu bán hàng.")
                continue

            # Tạo bản ghi trong SimDaBan
            try:
                SimDaBan.objects.create(
                    so_thu_tu=sim.so_thu_tu,
                    so_thue_bao=sim.so_thue_bao,
                    gia_thu_goc=sim.gia_thu_goc,
                    gia_chiet_khau=sim.gia_chiet_khau,
                    phi_giao_dich=sim.phi_giao_dich,
                    ngay_ban=sim.ngay_ban,
                    nguoi_ban=sim.nguoi_ban,
                    nha_mang=sim.nha_mang,
                )
                sim.trang_thai = 'Đã bán'
                sim.save()
                count += 1
            except Exception as e:
                errors.append(f"Lỗi khi xử lý SIM {sim.so_thue_bao}: {str(e)}")

        if errors:
            self.message_user(request, f"Có lỗi xảy ra:\n{', '.join(errors)}", level="error")
        self.message_user(request, f"Đã chuyển {count} SIM sang trạng thái 'Đã bán'.", level="success")

    chuyen_sang_da_ban.short_description = "Chuyển các SIM được chọn sang trạng thái 'Đã bán'"

    def formatted_gia_thu_goc(self, obj):
        return intcomma(obj.gia_thu_goc)
    formatted_gia_thu_goc.short_description = 'Giá Thu Gốc'

    def formatted_gia_chiet_khau(self, obj):
        return intcomma(obj.gia_chiet_khau)
    formatted_gia_chiet_khau.short_description = 'Giá Chiết Khấu'

# Admin cho SimDaBan
class SimDaBanAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = SimDaBanResource
    list_display = ('so_thu_tu', 'so_thue_bao', 'formatted_gia_thu_goc', 'formatted_gia_chiet_khau', 
                    'formatted_phi_giao_dich', 'formatted_thuc_thu', 'formatted_ngay_ban', 'nguoi_ban', 'nha_mang')
    search_fields = ('so_thue_bao', 'nguoi_ban', 'nha_mang')
    list_filter = ('ngay_ban', 'nha_mang')

    def formatted_gia_thu_goc(self, obj):
        return intcomma(obj.gia_thu_goc)
    formatted_gia_thu_goc.short_description = 'Giá Thu Gốc'

    def formatted_gia_chiet_khau(self, obj):
        return intcomma(obj.gia_chiet_khau)
    formatted_gia_chiet_khau.short_description = 'Giá Chiết Khấu'

    def formatted_phi_giao_dich(self, obj):
        return intcomma(obj.phi_giao_dich)
    formatted_phi_giao_dich.short_description = 'Phí Giao Dịch'

    def formatted_thuc_thu(self, obj):
        return intcomma(obj.thuc_thu)
    formatted_thuc_thu.short_description = 'Thực Thu'

    def formatted_ngay_ban(self, obj):
        """Hiển thị ngày bán theo định dạng DD/MM/YYYY"""
        return format(obj.ngay_ban, '%d-%m-%Y')  # Định dạng ngày
    formatted_ngay_ban.short_description = 'Ngày bán'  # Tiêu đề cột trong Admin

# Đăng ký các model vào admin
admin.site.register(SimTonKho, SimTonKhoAdmin)
admin.site.register(SimDaBan, SimDaBanAdmin)
