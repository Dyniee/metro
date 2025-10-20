// Đăng nhập User
document.getElementById('loginForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const loginData = {
        email: document.getElementById('email').value,
        password: document.getElementById('password').value
    };
    
    try {
        const response = await fetch(`${API_URL}/auth/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(loginData)
        });
        
        const data = await response.json();
        
        if (response.ok) {
            // === LƯU TOKEN VÀ THÔNG TIN USER ===
            saveToken(data.token); // (Từ common.js)
            localStorage.setItem('metro_user', JSON.stringify(data.user));
            
            showMessage('message', '✅ Đăng nhập thành công! Đang chuyển hướng...', 'success');
            
            // Chờ 2 giây rồi chuyển đến trang Mua Vé
            setTimeout(() => {
                window.location.href = 'buy_ticket.html'; 
            }, 2000);
            
        } else {
            showMessage('message', `❌ ${data.error}`, 'error');
        }
    } catch (error) {
        showMessage('message', `❌ Lỗi: ${error.message}`, 'error');
    }
});