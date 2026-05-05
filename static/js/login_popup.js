document.addEventListener('DOMContentLoaded', function () {
    const orderButton = document.querySelectorAll('#orderButton');
    const registerPopup = document.querySelector('.register-popup');
    const authPopup = document.querySelector('.auth-popup');


    const changeToAuth = document.querySelector('#changeToAuth');
    const changeToReg = document.querySelector('#changeToReg');
    const closeButtons = document.querySelectorAll('.close-popup');

    let isReg = true;

    function showNotification(message, isError = false) {
        const notification = document.createElement('div');
        notification.className = 'custom-notification';
        notification.textContent = message;
        notification.style.position = 'fixed';
        notification.style.top = '20px';
        notification.style.right = '20px';
        notification.style.padding = '10px 20px';
        notification.style.backgroundColor = isError ? '#ff4444' : '#4CAF50';
        notification.style.color = 'white';
        notification.style.borderRadius = '5px';
        notification.style.zIndex = '10000';
        notification.style.fontSize = '14px';

        document.body.appendChild(notification);

        setTimeout(() => {
            notification.remove();
        }, 3000);
    }

    function openPopup() {
        registerPopup.style.display = 'block';
        authPopup.style.display = 'none';
        isReg = true;
    }

    function closePopup() {
        registerPopup.style.display = 'none';
        authPopup.style.display = 'none';
    }

    async function handleRegisterSubmit(event) {
        event.preventDefault();

        const form = event.target;
        const name = form.querySelector('input[name="register-name"]').value.trim();
        const surname = form.querySelector('input[name="register-surname"]').value.trim();
        const email = form.querySelector('input[name="register-email"]').value.trim();
        const password = form.querySelector('input[name="register-password"]').value;
        const repPassword = form.querySelector('input[name="register-rep-password"]').value;

        if (!name || !surname || !email || !password || !repPassword) {
            showNotification('Заполните все поля', true);
            return;
        }

        if (password !== repPassword) {
            showNotification('Пароли не совпадают', true);
            return;
        }

        if (password.length < 6) {
            showNotification('Пароль должен быть не менее 6 символов', true);
            return;
        }

        try {
            const response = await fetch('/register', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    name: name,
                    surname: surname,
                    email: email,
                    password: password,
                    rep_password: repPassword
                })
            });

            const data = await response.json();

            if (data.success) {
                showNotification(data.message);
                setTimeout(() => {
                    window.location.href = data.redirect;
                }, 1000);
            } else {
                showNotification(data.message, true);
            }
        } catch (error) {
            console.error('Ошибка:', error);
            showNotification('Ошибка сервера', true);
        }
    }

    async function handleAuthSubmit(event) {
        event.preventDefault();

        const form = event.target;
        const email = form.querySelector('input[name="auth-mail"]').value.trim();
        const password = form.querySelector('input[name="auth-password"]').value;

        if (!email || !password) {
            showNotification('Заполните все поля', true);
            return;
        }

        try {
            const response = await fetch('/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    email: email,
                    password: password
                })
            });

            const data = await response.json();

            if (data.success) {
                showNotification(data.message);
                setTimeout(() => {
                    window.location.href = data.redirect;
                }, 1000);
            } else {
                showNotification(data.message, true);
            }
        } catch (error) {
            console.error('Ошибка:', error);
            showNotification('Ошибка сервера', true);
        }
    }

    async function checkAuth() {
        try {
            const response = await fetch('/check_auth');
            const data = await response.json();
            return data.authenticated;
        } catch (error) {
            console.error('Ошибка:', error);
            return false;
        }
    }


    const registerForm = document.querySelector('.reg-popup-form');
    const authForm = document.querySelector('.auth-popup-form');

    if (registerForm) registerForm.addEventListener('submit', handleRegisterSubmit);
    if (authForm) authForm.addEventListener('submit', handleAuthSubmit);


    orderButton.forEach(button => {
        button.addEventListener('click', async function (event) {
            event.preventDefault();
            const isAuth = await checkAuth();
            if (isAuth) {
                window.location.href = '/delivery';
            } else {
                openPopup();
            }
        });
    });

    registerPopup.addEventListener('click', event => { if (event.target === registerPopup) closePopup(); });
    authPopup.addEventListener('click', event => { if (event.target === authPopup) closePopup(); });

    document.addEventListener('keydown', event => {
        if (event.key === 'Escape' && (registerPopup.style.display === 'block' || authPopup.style.display === 'block')) {
            closePopup();
        }
    });

    closeButtons.forEach(button => button.addEventListener('click', (e) => { e.preventDefault(); closePopup(); }));

    if (changeToAuth) {
        changeToAuth.addEventListener('click', function (event) {
            event.preventDefault();
            registerPopup.style.display = 'none';
            authPopup.style.display = 'block';
            isReg = false;
        });
    }

    if (changeToReg) {
        changeToReg.addEventListener('click', function (event) {
            event.preventDefault();
            registerPopup.style.display = 'block';
            authPopup.style.display = 'none';
            isReg = true;
        });
    }
});
