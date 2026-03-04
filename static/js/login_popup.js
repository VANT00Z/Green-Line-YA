document.addEventListener('DOMContentLoaded', function () {
    const mainOrder = document.querySelectorAll('#order-button');
    const registerPopup = document.querySelector('.register-popup');
    const authPopup = document.querySelector('.auth-popup');
    const changeButtons = document.querySelectorAll('#change-button');
    const closeButton = document.querySelector('.close-popup');
    let isReg = true

    // open
    function openPopup() {
        registerPopup.style.display = 'block';
        authPopup.style.display = 'none';
        isReg = true;
    }

    // close
    function closePopup() {
        registerPopup.style.display = 'none';
        authPopup.style.display = 'none';
    }

    mainOrder.forEach(button => {
        button.addEventListener('click', function (event) {
            event.preventDefault();
            openPopup();
        });
    });

    // Закрытие popup при клике на затемненную область
    registerPopup.addEventListener('click', function (event) {
        if (event.target === registerPopup) {
            closePopup();
        }
    });

    authPopup.addEventListener('click', function (event) {
        if (event.target === authPopup) {
            closePopup();
        }
    });

    document.addEventListener('keydown', function (event) {
        if (event.key === 'Escape' &&
            (registerPopup.style.display === 'block' || authPopup.style.display === 'block')) {
            closePopup();
        }
    });

    closeButton.addEventListener('click', closePopup);

    changeButtons.forEach(button => {
        button.addEventListener('click', function (event) {
            event.preventDefault();
            if (isReg) {
                registerPopup.style.display = 'none';
                authPopup.style.display = 'block';
                isReg = false;
            } else {
                registerPopup.style.display = 'block';
                authPopup.style.display = 'none';
                isReg = true;
            }
        });
    });
});