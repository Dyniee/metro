// Đăng ký User
document.getElementById('registerForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    // === CẬP NHẬT LẠI DỮ LIỆU GỬI ĐI ===
    const userData = {
        username: document.getElementById('username').value,
        email: document.getElementById('email').value,
        password: document.getElementById('password').value, 
        phone: document.getElementById('phone').value,
        initial_balance: parseFloat(document.getElementById('balance').value) // <-- THÊM LẠI DÒNG NÀY
    };
    
    try {
        const response = await fetch(`${API_URL}/auth/register`, { 
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(userData)
        });
        
        const data = await response.json();
        
        if (response.ok) {
            // Hiện form thành công
            document.getElementById('registerForm').style.display = 'none';
            document.getElementById('successInfo').style.display = 'block';
            
            showMessage('message', `✅ Đăng ký thành công!`, 'success');
        } else {
            showMessage('message', `❌ ${data.error}`, 'error');
        }
    } catch (error) {
        showMessage('message', `❌ Lỗi: ${error.message}`, 'error');
    }
});