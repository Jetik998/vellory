document.addEventListener('DOMContentLoaded', function () {
    const loginForm = document.getElementById('loginForm');
    const usernameInput = document.getElementById('username');
    const passwordInput = document.getElementById('password');
    const logoutButton = document.getElementById('logoutButton');
    const

    // форма логина
    if (loginForm && usernameInput && passwordInput) {
        usernameInput.addEventListener('input', function () {
            const value = usernameInput.value.trim();
            if (value.includes('@')) {
                const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
                usernameInput.setCustomValidity(
                    emailPattern.test(value)
                        ? ''
                        : 'Введите корректный email (должна быть точка после @)'
                );
            } else {
                usernameInput.setCustomValidity('');
            }
        });

        loginForm.addEventListener('submit', async function (event) {
            event.preventDefault();
            if (!loginForm.checkValidity()) {
                loginForm.reportValidity();
                return;
            }
            const requestBody = new URLSearchParams({
                username: usernameInput.value,
                password: passwordInput.value
            });
            try {
                const response = await fetch('/api/auth/token-cookie', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/x-www-form-urlencoded'},
                    body: requestBody,
                    credentials: 'include'
                });
                if (response.ok) {
                    window.location.reload();
                } else {
                    const errorData = await response.json();
                    alert('Ошибка входа: ' + (errorData.detail || 'Неверные данные'));
                }
            } catch {
                alert('Ошибка соединения с сервером');
            }
        });
    }

    // кнопка выхода
    if (logoutButton) {
        logoutButton.addEventListener('click', async function () {
            try {
                const response = await fetch('/logout', {
                    method: 'POST',
                    credentials: 'include'
                });
                if (response.ok) {
                    window.location.reload();
                } else {
                    alert('Ошибка при выходе');
                }
            } catch (error) {
                console.error('Ошибка выхода:', error);
            }
        });
    }
});


