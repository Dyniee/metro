// Tự động tải lịch sử khi trang được mở
document.addEventListener('DOMContentLoaded', loadHistory);

async function loadHistory() {
    // 1. Kiểm tra Token
    const token = getToken();
    if (!token) {
        // Nếu chưa đăng nhập, đá về trang login
        showMessage('message', '❌ Bạn phải đăng nhập để xem lịch sử. Đang chuyển hướng...', 'error');
        setTimeout(() => {
            window.location.href = 'login.html';
        }, 2000);
        return;
    }

    // 2. Gọi API (có đính kèm Token)
    try {
        const response = await fetch(`${API_URL}/ticket/history`, {
            method: 'GET',
            headers: getAuthHeaders(false) // <-- Lấy header có Token từ common.js
        });

        const data = await response.json();

        if (response.ok) {
            displayUserInfo(data.user);
            displayHistory(data.history);
        } else {
            // Lỗi (ví dụ: Token hết hạn)
            showMessage('message', `❌ ${data.error}`, 'error');
            if (response.status === 401) {
                // Nếu Token hỏng, bắt đăng xuất
                logout();
            }
        }
    } catch (error) {
        showMessage('message', `❌ Lỗi mạng: ${error.message}`, 'error');
    }
}

// Hiển thị thông tin user
function displayUserInfo(user) {
    document.getElementById('infoUsername').textContent = user.username;
    document.getElementById('infoBalance').textContent = formatCurrency(user.wallet_balance);
    document.getElementById('userInfo').style.display = 'block';
}

// Hiển thị lịch sử (cập nhật các cột mới)
function displayHistory(history) {
    const tbody = document.getElementById('historyBody');
    tbody.innerHTML = '';
    
    if (history.length === 0) {
        document.getElementById('historyTable').style.display = 'none';
        document.getElementById('emptyMessage').style.display = 'block';
        return;
    }
    
    document.getElementById('historyTable').style.display = 'table';
    document.getElementById('emptyMessage').style.display = 'none';
    
    history.forEach(ticket => {
        const row = tbody.insertRow();
        
        // Định dạng lại Giờ đi cho đẹp
        const validTime = new Date(ticket.valid_at_datetime).toLocaleString('vi-VN', {
            year: 'numeric', month: '2-digit', day: '2-digit',
            hour: '2-digit', minute: '2-digit'
        });
        
        row.innerHTML = `
            <td>${formatDate(ticket.created_at)}</td>
            <td>${ticket.station_from_name}</td>
            <td>${ticket.station_to_name}</td>
            <td>${validTime}</td>
            <td>${formatCurrency(ticket.purchase_price)}</td>
            <td>${ticket.status}</td>
        `;
    });
}