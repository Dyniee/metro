// ===================================
// === LOGIC KIOSK CHECK-IN (MỚI) ===
// ===================================

// Biến toàn cục
let stream = null;
const videoEl = document.getElementById('videoKiosk');
const canvasEl = document.getElementById('canvasKiosk');
const kioskStationSelect = document.getElementById('kioskStation');
const checkButton = document.getElementById('checkButton');
const messageEl = document.getElementById('messageKiosk');

// Biến cho modal kết quả (từ bước trước)
const resultOverlay = document.getElementById('resultOverlay');
const resultBox = document.getElementById('resultBox');
const resultIcon = document.getElementById('resultIcon');
const resultUsername = document.getElementById('resultUsername');
const resultInfo = document.getElementById('resultInfo');

// === KHỞI ĐỘNG KIOSK ===
document.addEventListener('DOMContentLoaded', () => {
    loadStations();
    startCamera();
});

// 1. Tải danh sách Ga
async function loadStations() {
    try {
        const response = await fetch(`${API_URL}/ticket/stations`);
        const stations = await response.json();
        
        kioskStationSelect.innerHTML = '<option value="">-- Chọn Ga Hiện Tại --</option>';
        stations.forEach(station => {
            kioskStationSelect.add(new Option(`${station.station_name} (ID: ${station.station_id})`, station.station_id));
        });
    } catch (error) {
        showMessage('messageKiosk', `❌ Lỗi tải ga: ${error.message}`, 'error');
    }
}

// 2. Tự động bật Camera
async function startCamera() {
    try {
        stream = await navigator.mediaDevices.getUserMedia({ video: true });
        videoEl.srcObject = stream;
    } catch (err) {
        showMessage('messageKiosk', `❌ Lỗi camera: ${err.message}`, 'error');
    }
}

// 3. Nút "Kiểm Tra" (Giả lập việc Kiosk tự động quét)
checkButton.addEventListener('click', () => {
    // Kiểm tra ga
    const kioskStationId = kioskStationSelect.value;
    if (!kioskStationId) {
        showMessage('messageKiosk', '❌ Vui lòng chọn ga cho Kiosk này', 'error');
        return;
    }

    // Chụp ảnh
    const context = canvasEl.getContext('2d');
    canvasEl.width = videoEl.videoWidth;
    canvasEl.height = videoEl.videoHeight;
    context.drawImage(videoEl, 0, 0, canvasEl.width, canvasEl.height);
    
    // Chuyển ảnh sang Blob
    canvasEl.toBlob(blob => {
        // Gọi API kiểm tra
        checkFace(kioskStationId, blob);
    }, 'image/jpeg', 0.95);
});

// 4. Gọi API /kiosk/check
async function checkFace(stationId, imageBlob) {
    const formData = new FormData();
    formData.append('station_id', stationId);
    
    // Chuyển Blob thành File
    const imageFile = new File([imageBlob], "kiosk_capture.jpg", { type: "image/jpeg" });
    formData.append('image', imageFile);
    
    try {
        const response = await fetch(`${API_URL}/kiosk/check`, { // <-- GỌI API KIOSK MỚI
            method: 'POST',
            body: formData
            // (Không cần Token cho Kiosk)
        });

        const data = await response.json();

        if (response.ok) {
            // HIỆN MÀN HÌNH XANH
            showResult(true, data);
        } else {
            // HIỆN MÀN HÌNH ĐỎ
            showResult(false, data);
        }

    } catch (error) {
        showResult(false, { error: `Lỗi mạng: ${error.message}` });
    }
}


// 5. Hàm Hiển Thị Kết Quả (Xanh/Đỏ)
function showResult(isSuccess, data) {
    if (isSuccess) {
        // --- MÀN HÌNH XANH (THÀNH CÔNG) ---
        resultBox.className = 'result-box success';
        resultIcon.textContent = '✅';
        resultUsername.textContent = data.user.username; // Tên user
        resultInfo.textContent = `Ga Đến: ${data.ticket.station_to_name}`; // Ga đến
    } else {
        // --- MÀN HÌNH ĐỎ (THẤT BẠI) ---
        resultBox.className = 'result-box error';
        resultIcon.textContent = '❌';
        resultUsername.textContent = 'Không Hợp Lệ';
        resultInfo.textContent = data.error || 'Lỗi không xác định'; // Lý do lỗi
    }
    
    // Hiển thị overlay
    resultOverlay.classList.add('show');
    
    // Tự động ẩn sau 3.5 giây
    setTimeout(() => {
        resultOverlay.classList.remove('show');
    }, 3500);
}

// Hàm showMessage (để báo lỗi nhỏ)
function showMessage(elementId, message, type = 'info') {
    const msgEl = document.getElementById(elementId);
    if (!msgEl) return;
    
    msgEl.textContent = message;
    msgEl.className = `message show ${type}`;
    
    setTimeout(() => {
        msgEl.classList.remove('show');
    }, 4000);
}