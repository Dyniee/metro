// ========== GLOBAL CONFIG ==========
const API_URL = 'http://localhost:5000/api';

// ========== UTILITY FUNCTIONS ==========
function showMessage(elementId, message, type = 'info') {
    const msgEl = document.getElementById(elementId);
    if (!msgEl) return;
    
    msgEl.textContent = message;
    msgEl.className = `message show ${type}`;
    
    setTimeout(() => {
        msgEl.classList.remove('show');
    }, 5000);
}

function previewImage(inputId, previewId) {
    const input = document.getElementById(inputId);
    if (!input) return;
    
    input.addEventListener('change', (e) => {
        const file = e.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = (event) => {
                const preview = document.getElementById(previewId);
                if (preview) {
                    preview.src = event.target.result;
                    preview.style.display = 'block';
                }
            };
            reader.readAsDataURL(file);
        }
    });
}

function formatCurrency(value) {
    return new Intl.NumberFormat('vi-VN', {
        style: 'currency',
        currency: 'VND',
        minimumFractionDigits: 0
    }).format(value);
}

function formatDate(dateString) {
    return new Date(dateString).toLocaleString('vi-VN', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit'
    });
}

// Setup image previews globally
document.addEventListener('DOMContentLoaded', () => {
    // Register Face page
    previewImage('faceImage', 'previewImg');
    
    // Upload Face page
    previewImage('recognizeImage', 'previewImg');
    
    // Buy Ticket page
    previewImage('imageIn', 'previewIn');
    previewImage('imageOut', 'previewOut');
});