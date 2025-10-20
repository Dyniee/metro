// Nhận diện Khuôn Mặt
document.getElementById('recognizeForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const imageInput = document.getElementById('recognizeImage');
    
    if (!imageInput.files[0]) {
        showMessage('message', '❌ Vui lòng chọn ảnh', 'error');
        return;
    }
    
    const formData = new FormData();
    formData.append('image', imageInput.files[0]);
    
    try {
        const response = await fetch(`${API_URL}/face/recognize`, {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (response.ok) {
            // Hiện thông tin người dùng
            document.getElementById('resultInfo').style.display = 'block';
            document.getElementById('resultUsername').textContent = data.user.username;
            document.getElementById('resultEmail').textContent = data.user.email;
            document.getElementById('resultPhone').textContent = data.user.phone || 'Chưa cập nhật';
            document.getElementById('resultBalance').textContent = formatCurrency(data.user.wallet_balance);
            document.getElementById('resultConfidence').textContent = data.confidence;
            
            // Lưu user ID
            localStorage.setItem('recognizedUserId', data.user.user_id);
            
            showMessage('message', '✅ Nhận diện thành công!', 'success');
        } else {
            showMessage('message', `❌ ${data.error}`, 'error');
        }
    } catch (error) {
        showMessage('message', `❌ Lỗi: ${error.message}`, 'error');
    }
});