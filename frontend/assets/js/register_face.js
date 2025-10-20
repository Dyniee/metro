/* // Đăng ký Khuôn Mặt
document.getElementById('registerFaceForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const userId = document.getElementById('userId').value;
    const imageInput = document.getElementById('faceImage');
    
    if (!userId || !imageInput.files[0]) {
        showMessage('message', '❌ Vui lòng điền đầy đủ thông tin', 'error');
        return;
    }
    
    const formData = new FormData();
    formData.append('image', imageInput.files[0]);
    
    try {
        const response = await fetch(`${API_URL}/face/register/${userId}`, {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (response.ok) {
            // Hiện form thành công
            document.getElementById('registerFaceForm').style.display = 'none';
            document.getElementById('successInfo').style.display = 'block';
            
            document.getElementById('faceId').textContent = data.face_data.face_id;
            document.getElementById('successUserId').textContent = userId;
            
            // Lưu vào localStorage
            localStorage.setItem('lastFaceId', data.face_data.face_id);
            
            showMessage('message', '✅ Đăng ký khuôn mặt thành công!', 'success');
        } else {
            showMessage('message', `❌ ${data.error}`, 'error');
        }
    } catch (error) {
        showMessage('message', `❌ Lỗi: ${error.message}`, 'error');
    }
}); */