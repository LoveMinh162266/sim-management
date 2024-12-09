// URL của API backend
const API_URL = '/api/sim-da-ban/';

// Lấy danh sách sim đã bán và hiển thị vào bảng
function fetchSimDaBan() {
    fetch(API_URL)
        .then(response => response.json())
        .then(data => {
            let tableBody = document.getElementById('simDaBanTable');
            tableBody.innerHTML = ''; // Xóa nội dung cũ

            data.forEach((sim, index) => {
                const thucThu = sim.gia_chiet_khau - sim.phi_giao_dich; // Tính thực thu

                tableBody.innerHTML += `
                    <tr>
                        <td>${index + 1}</td>
                        <td>${sim.so_thue_bao}</td>
                        <td>${sim.gia_thu_goc}</td>
                        <td>${sim.gia_chiet_khau}</td>
                        <td>${sim.phi_giao_dich}</td>
                        <td>${thucThu}</td>
                        <td>${sim.ngay_ban}</td>
                        <td>${sim.nguoi_ban}</td>
                        <td>${sim.nha_mang}</td>
                    </tr>
                `;
            });
        })
        .catch(error => console.error('Lỗi khi gọi API:', error));
}

// Gọi API để lấy danh sách sim khi tải trang
document.addEventListener('DOMContentLoaded', fetchSimDaBan);
