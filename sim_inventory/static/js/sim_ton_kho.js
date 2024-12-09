const SIM_TON_KHO_API_URL = '/api/sim-ton-kho/'; // Đảm bảo URL đúng

// Lấy danh sách sim tồn kho và hiển thị vào bảng
function fetchSimTonKho(page = 1) {
    fetch(`${SIM_TON_KHO_API_URL}?page=${page}`)
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            console.log('Dữ liệu trả về từ API:', data);

            if (!data || !Array.isArray(data.results) || data.results.length === 0) {
                handleEmptyData(data);
                return;
            }

            populateSimTonKhoTable(data.results, data.count, page);
            updatePagination(data, page);
        })
        .catch(error => {
            console.error('Lỗi khi gọi API:', error);
            displayError('Đã xảy ra lỗi khi tải dữ liệu. Vui lòng thử lại sau.');
        });
}

// Xử lý khi dữ liệu trống hoặc không hợp lệ
function handleEmptyData(data) {
    console.warn('Dữ liệu không hợp lệ hoặc trống:', data);
    let tableBody = document.getElementById('simTonKhoTable');
    tableBody.innerHTML = '<tr><td colspan="7">Không có dữ liệu sim tồn kho.</td></tr>';
}

// Hiển thị dữ liệu vào bảng
function populateSimTonKhoTable(results, totalCount, page) {
    let tableBody = document.getElementById('simTonKhoTable');
    tableBody.innerHTML = '';

    results.forEach((sim, index) => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${index + 1 + (page - 1) * results.length}</td>
            <td>${sim.so_thue_bao}</td>
            <td>${sim.gia_thu_goc}</td>
            <td>${sim.gia_chiet_khau}</td>
            <td>${sim.nha_mang}</td>
            <td>${sim.trang_thai}</td>
            <td>
                <button class="btn btn-success" onclick="markAsSold(${sim.so_thu_tu})">Bán</button>
            </td>
        `;
        tableBody.appendChild(row);
    });
}

// Cập nhật phần điều hướng phân trang
function updatePagination(data, currentPage) {
    let paginationDiv = document.getElementById('pagination');
    paginationDiv.innerHTML = '';

    // Nút trang trước
    if (data.previous) {
        paginationDiv.innerHTML += `
            <button onclick="fetchSimTonKho(${currentPage - 1})">&laquo; Trang trước</button>
        `;
    }

    // Các nút trang
    let totalPages = Math.ceil(data.count / 20); 
    for (let i = 1; i <= totalPages; i++) {
        paginationDiv.innerHTML += `
            <button onclick="fetchSimTonKho(${i})">${i}</button>
        `;
    }

    // Nút trang tiếp theo
    if (data.next) {
        paginationDiv.innerHTML += `
            <button onclick="fetchSimTonKho(${currentPage + 1})">Trang tiếp theo &raquo;</button>
        `;
    }
}
function chuyenSim(so_thu_tu) {
    // Lấy ngày bán từ input
    const ngayBan = document.getElementById('ngay_ban').value; // Giả sử có input với id 'ngay_ban'
    const nguoiBan = document.getElementById('nguoi_ban').value;
    const phiGiaoDich = document.getElementById('phi_giao_dich').value;
    // Kiểm tra nếu ngày bán hợp lệ
    if (!ngayBan) {
        alert('Vui lòng nhập ngày bán');
        return;
    }

    fetch(`/chuyen-trang-thai/${so_thu_tu}/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            ngay_ban: ngayBan, // Gửi ngày bán với định dạng hợp lệ
            nguoi_ban: nguoiBan, 
            phi_giao_dich: phiGiaoDich,
        })
    })
    .then(response => {
        if (response.ok) {
            alert('Sim đã chuyển sang trạng thái đã bán!');
            fetchSimTonKho(); 
        } else {
            alert('Đã có lỗi khi chuyển trạng thái.');
        }
    })
    .catch(error => {
        console.error('Lỗi khi gọi API:', error);
        alert('Đã có lỗi xảy ra!');
    });
}
