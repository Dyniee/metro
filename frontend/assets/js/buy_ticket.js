// Biến toàn cục
let capturedImageBase64 = null; // Lưu ảnh đã chụp
let stream = null;

// ===================================
// === KIỂM TRA ĐĂNG NHẬP VÀ TẢI DỮ LIỆU ===
// ===================================
document.addEventListener('DOMContentLoaded', async () => {
    const token = getToken();
    if (!token) {
        showMessage('message', '❌ Bạn phải đăng nhập. Đang chuyển hướng...', 'error');
        setTimeout(() => window.location.href = 'login.html', 2000);
        return;
    }
    loadUserInfo();
    await loadStations();
});

function loadUserInfo() {
    const userString = localStorage.getItem('metro_user');
    if (!userString) {
        logout(); // (Từ common.js)
        return;
    }
    
    const user = JSON.parse(userString);
    
    document.getElementById('userInfo').style.display = 'block';
    document.getElementById('infoUsername').textContent = user.username;
    document.getElementById('infoBalance').textContent = formatCurrency(user.wallet_balance);
    
    // === CẬP NHẬT CHỖ NÀY ===
    // Kiểm tra xem user đã có ảnh chưa
    fetch(`${API_URL}/auth/user/${user.user_id}`, { headers: getAuthHeaders(false) })
        .then(res => {
            // Nếu nhận 401 (Token hỏng), tự động logout
            if (res.status === 401) {
                showMessage('message', '❌ Phiên đăng nhập hết hạn. Vui lòng đăng nhập lại.', 'error');
                setTimeout(logout, 2000);
                return null; // Dừng xử lý
            }
            return res.json();
        })
        .then(data => {
            if (data && (data.face_data === null || data.face_data === undefined)) {
                // Nếu CHƯA có ảnh, hiện mục camera
                document.getElementById('cameraSection').style.display = 'block';
            }
        })
        .catch(err => {
            console.error("Lỗi kiểm tra face_data:", err);
        });
}

// Hàm loadStations (Giữ nguyên)
async function loadStations() {
    try {
        const response = await fetch(`${API_URL}/ticket/stations`);
        const stations = await response.json();
        
        const selectFrom = document.getElementById('stationFrom');
        const selectTo = document.getElementById('stationTo');
        
        selectFrom.innerHTML = '<option value="">-- Chọn Ga Đi --</option>';
        selectTo.innerHTML = '<option value="">-- Chọn Ga Đến --</option>';
        
        stations.forEach(station => {
            selectFrom.add(new Option(`${station.station_name} (ID: ${station.station_id})`, station.station_id));
            selectTo.add(new Option(`${station.station_name} (ID: ${station.station_id})`, station.station_id));
        });
    } catch (error) {
        showMessage('message', `❌ Lỗi tải danh sách ga: ${error.message}`, 'error');
    }
}

// Logic Camera (Giữ nguyên)
document.getElementById('startCamera').addEventListener('click', async () => {
    try {
        const videoEl = document.getElementById('videoCapture');
        stream = await navigator.mediaDevices.getUserMedia({ video: true });
        videoEl.srcObject = stream;
        videoEl.style.display = 'block';
        document.getElementById('startCamera').style.display = 'none';
        document.getElementById('captureImage').style.display = 'block';
    } catch (err) {
        showMessage('message', `❌ Lỗi camera: ${err.message}`, 'error');
    }
});

document.getElementById('captureImage').addEventListener('click', () => {
    // ... (Giữ nguyên code chụp ảnh) ...
    const videoEl = document.getElementById('videoCapture');
    const canvas = document.getElementById('canvasCapture');
    const context = canvas.getContext('2d');
    canvas.width = videoEl.videoWidth;
    canvas.height = videoEl.videoHeight;
    context.drawImage(videoEl, 0, 0, canvas.width, canvas.height);
    capturedImageBase64 = canvas.toDataURL('image/jpeg', 0.9);
    document.getElementById('previewImg').src = capturedImageBase64;
    document.getElementById('previewImg').style.display = 'block';
    stream.getTracks().forEach(track => track.stop());
    videoEl.style.display = 'none';
    document.getElementById('captureImage').style.display = 'none';
    showMessage('message', '✅ Đã chụp ảnh!', 'success');
});


// ===================================
// === SUBMIT MUA VÉ (CẬP NHẬT) ===
// ===================================
document.getElementById('buyTicketForm').addEventListener('submit', async (e) => {
    e.preventDefault();

    // ... (Code lấy dữ liệu form giữ nguyên) ...
    const stationFromId = document.getElementById('stationFrom').value;
    const stationToId = document.getElementById('stationTo').value;
    const date = document.getElementById('ticketDate').value;
    const time = document.getElementById('ticketTime').value;

    if (!stationFromId || !stationToId || !date || !time) {
        showMessage('message', '❌ Vui lòng điền đầy đủ thông tin vé.', 'error');
        return;
    }
    
    let isoDateTime;
    try {
        const localDate = new Date(`${date}T${time}`);
        isoDateTime = localDate.toISOString();
    } catch (err) {
        showMessage('message', '❌ Ngày hoặc Giờ không hợp lệ.', 'error');
        return;
    }

    const ticketData = {
        station_from_id: parseInt(stationFromId),
        station_to_id: parseInt(stationToId),
        valid_at_datetime: isoDateTime,
        face_images: []
    };

    const cameraSectionVisible = document.getElementById('cameraSection').style.display === 'block';
    if (cameraSectionVisible) {
        if (!capturedImageBase64) {
            showMessage('message', '❌ Vui lòng chụp ảnh khuôn mặt.', 'error');
            return;
        }
        ticketData.face_images.push(capturedImageBase64);
    }
    
    // 5. Gửi API (có kèm Token)
    try {
        const response = await fetch(`${API_URL}/ticket/buy`, {
            method: 'POST',
            headers: getAuthHeaders(),
            body: JSON.stringify(ticketData)
        });

        const data = await response.json();

        if (response.ok) {
            showMessage('message', `✅ Mua vé thành công! (ID: ${data.ticket.ticket_id})`, 'success');
            // Cập nhật lại số dư ví hiển thị
            localStorage.setItem('metro_user', JSON.stringify(data.user)); // Cập nhật user mới
            document.getElementById('infoBalance').textContent = formatCurrency(data.new_balance);
            document.getElementById('cameraSection').style.display = 'none';
        } else {
            // === XỬ LÝ LỖI 401 (CẬP NHẬT Ở ĐÂY) ===
            showMessage('message', `❌ Lỗi: ${data.error}`, 'error');
            if (response.status === 401) {
                // Nếu là lỗi 401, tự động logout
                showMessage('message', '❌ Phiên đăng nhập hết hạn. Vui lòng đăng nhập lại.', 'error');
                setTimeout(logout, 2000); // Gọi logout() từ common.js
            }
            // ===================================
        }

    } catch (error) {
        showMessage('message', `❌ Lỗi mạng: ${error.message}`, 'error');
    }
});
/* 
// Biến toàn cục
let capturedImageBase64 = null; // Lưu ảnh đã chụp
let stream = null;

// ===================================
// === KIỂM TRA ĐĂNG NHẬP VÀ TẢI DỮ LIỆU ===
// ===================================
document.addEventListener('DOMContentLoaded', async () => {
    const token = getToken();
    if (!token) {
        showMessage('message', '❌ Bạn phải đăng nhập. Đang chuyển hướng...', 'error');
        setTimeout(() => window.location.href = 'login.html', 2000);
        return;
    }
    loadUserInfo();
    await loadStations();
});

function loadUserInfo() {
    const userString = localStorage.getItem('metro_user');
    if (!userString) {
        logout(); // (Từ common.js)
        return;
    }

    const user = JSON.parse(userString);

    document.getElementById('userInfo').style.display = 'block';
    document.getElementById('infoUsername').textContent = user.username;
    document.getElementById('infoBalance').textContent = formatCurrency(user.wallet_balance);

    // Kiểm tra xem user đã có ảnh chưa (qua API)
    fetch(`${API_URL}/auth/user/${user.user_id}`, { headers: getAuthHeaders(false) })
        .then(res => {
            if (res.status === 401) {
                showMessage('message', '❌ Phiên đăng nhập hết hạn. Vui lòng đăng nhập lại.', 'error');
                setTimeout(logout, 2000);
                return null;
            }
            return res.json();
        })
        .then(data => {
            // KIỂM TRA XEM USER CÓ FACE_DATA CHƯA
            // Cần sửa API /auth/user/<id> để trả về face_data relationship
            // Tạm thời dựa vào giả định là API sẽ trả về
            if (data && (!data.face_data)) { // Nếu API trả về null hoặc không có key face_data
                 document.getElementById('cameraSection').style.display = 'block';
            }
        })
        .catch(err => {
            console.error("Lỗi kiểm tra face_data:", err);
            // Optionally show an error message, but don't force logout for this specific error
            // showMessage('message', '❌ Không thể kiểm tra trạng thái khuôn mặt.', 'error');
        });
}


async function loadStations() {
    try {
        const response = await fetch(`${API_URL}/ticket/stations`);
        const stations = await response.json();

        const selectFrom = document.getElementById('stationFrom');
        const selectTo = document.getElementById('stationTo');

        selectFrom.innerHTML = '<option value="">-- Chọn Ga Đi --</option>';
        selectTo.innerHTML = '<option value="">-- Chọn Ga Đến --</option>';

        stations.forEach(station => {
            selectFrom.add(new Option(`${station.station_name} (ID: ${station.station_id})`, station.station_id));
            selectTo.add(new Option(`${station.station_name} (ID: ${station.station_id})`, station.station_id));
        });
    } catch (error) {
        showMessage('message', `❌ Lỗi tải danh sách ga: ${error.message}`, 'error');
    }
}

// Logic Camera
document.getElementById('startCamera')?.addEventListener('click', async () => { // Thêm ? để tránh lỗi nếu element không tồn tại
    try {
        const videoEl = document.getElementById('videoCapture');
        stream = await navigator.mediaDevices.getUserMedia({ video: true });
        videoEl.srcObject = stream;
        videoEl.style.display = 'block';
        document.getElementById('startCamera').style.display = 'none';
        document.getElementById('captureImage').style.display = 'block';
    } catch (err) {
        showMessage('message', `❌ Lỗi camera: ${err.message}`, 'error');
    }
});

document.getElementById('captureImage')?.addEventListener('click', () => { // Thêm ?
    const videoEl = document.getElementById('videoCapture');
    const canvas = document.getElementById('canvasCapture');
    const context = canvas.getContext('2d');
    canvas.width = videoEl.videoWidth;
    canvas.height = videoEl.videoHeight;
    context.drawImage(videoEl, 0, 0, canvas.width, canvas.height);
    capturedImageBase64 = canvas.toDataURL('image/jpeg', 0.9);
    document.getElementById('previewImg').src = capturedImageBase64;
    document.getElementById('previewImg').style.display = 'block';
    if(stream) stream.getTracks().forEach(track => track.stop());
    videoEl.style.display = 'none';
    document.getElementById('captureImage').style.display = 'none';
    showMessage('message', '✅ Đã chụp ảnh!', 'success');
});


// Submit Mua Vé
document.getElementById('buyTicketForm')?.addEventListener('submit', async (e) => { // Thêm ?
    e.preventDefault();

    const stationFromId = document.getElementById('stationFrom').value;
    const stationToId = document.getElementById('stationTo').value;
    const date = document.getElementById('ticketDate').value;
    const time = document.getElementById('ticketTime').value;

    if (!stationFromId || !stationToId || !date || !time) {
        showMessage('message', '❌ Vui lòng điền đầy đủ thông tin vé.', 'error');
        return;
    }

    let isoDateTime;
    try {
        const localDate = new Date(`${date}T${time}`);
        if (isNaN(localDate)) throw new Error("Invalid Date/Time");
        isoDateTime = localDate.toISOString();
    } catch (err) {
        showMessage('message', '❌ Ngày hoặc Giờ không hợp lệ.', 'error');
        return;
    }

    const ticketData = {
        station_from_id: parseInt(stationFromId),
        station_to_id: parseInt(stationToId),
        valid_at_datetime: isoDateTime,
        face_images: []
    };

    const cameraSectionVisible = document.getElementById('cameraSection')?.style.display === 'block'; // Thêm ?
    if (cameraSectionVisible) {
        if (!capturedImageBase64) {
            showMessage('message', '❌ Vui lòng chụp ảnh khuôn mặt.', 'error');
            return;
        }
        ticketData.face_images.push(capturedImageBase64);
    }

    try {
        const response = await fetch(`${API_URL}/ticket/buy`, {
            method: 'POST',
            headers: getAuthHeaders(),
            body: JSON.stringify(ticketData)
        });

        const data = await response.json();

        if (response.ok) {
            showMessage('message', `✅ Mua vé thành công! (ID: ${data.ticket.ticket_id})`, 'success');
            // CẬP NHẬT LẠI USER TRONG LOCALSTORAGE VỚI SỐ DƯ MỚI
            // API `/ticket/buy` trả về user với balance mới
            const updatedUser = data.user;
            localStorage.setItem('metro_user', JSON.stringify(updatedUser));
            document.getElementById('infoBalance').textContent = formatCurrency(updatedUser.wallet_balance);

            document.getElementById('cameraSection')?.style.display = 'none'; // Thêm ?
        } else {
            showMessage('message', `❌ Lỗi: ${data.error}`, 'error');
            if (response.status === 401) {
                showMessage('message', '❌ Phiên đăng nhập hết hạn. Vui lòng đăng nhập lại.', 'error');
                setTimeout(logout, 2000);
            }
        }
    } catch (error) {
        showMessage('message', `❌ Lỗi mạng: ${error.message}`, 'error');
    }
});

// Ngừng camera nếu người dùng rời trang
window.addEventListener('beforeunload', () => {
    if (stream) {
        stream.getTracks().forEach(track => track.stop());
    }
}); */