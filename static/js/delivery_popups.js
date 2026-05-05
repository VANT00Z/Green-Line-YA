document.addEventListener('DOMContentLoaded', function () {
    // Buttons
    const deliveryButton = document.querySelectorAll('#open-order-popup');
    const historyButton = document.querySelectorAll('#open-history-popup');
    const activeButton = document.querySelectorAll('#open-active-popup');
    const closeButton = document.querySelector('.close-popup');

    // Popups
    const deliveryPopup = document.getElementById('delivery-popup');
    const historyPopup = document.getElementById('history-popup');
    const activePopup = document.getElementById('active-popup');

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

    async function handleOrderCreate(event) {
        event.preventDefault();

        const form = event.target;
        const adress = form.querySelector().value;
        const datetime = form.querySelector().value;
        const weight = form.querySelector().value;
        const description = form.querySelector().value;

        if (!adress || !datetime || !weight) {
            showNotification('Заполните обязательные поля', true)
        }
        try {
            const response = await fetch('/create_order', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    adress: adress,
                    datetime: datetime,
                    weight: weight,
                    description: description
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

    // open funcs
    function openDeliveryPopup() {
        deliveryPopup.style.display = 'block';
        closeHistoryPopup();
        closeActivePopup();
    }

    function openHistoryPopup() {
        if (historyPopup) historyPopup.style.display = 'block';
        closeDeliveryPopup();
        closeActivePopup();
    }

    function openActivePopup() {
        if (activePopup) activePopup.style.display = 'block';
        closeDeliveryPopup();
        closeHistoryPopup();
    }

    // close funcs
    function closeDeliveryPopup() {
        if (deliveryPopup) deliveryPopup.style.display = 'none';
    }

    function closeHistoryPopup() {
        if (historyPopup) historyPopup.style.display = 'none';
    }

    function closeActivePopup() {
        if (activePopup) activePopup.style.display = 'none';
    }

    function closeAll() {
        closeDeliveryPopup();
        closeHistoryPopup();
        closeActivePopup();
    }

    document.addEventListener('keydown', function (event) {
        if (event.key == 'Escape') {
            closeAll();
        }
    });

    if (closeButton) {
        closeButton.addEventListener('click', closeAll);
    }

    // other
    if (deliveryButton.length > 0) {
        deliveryButton.forEach(button => {
            button.addEventListener('click', function (event) {
                event.preventDefault();
                openDeliveryPopup();
            });
        });
    }

    if (historyButton.length > 0) {
        historyButton.forEach(button => {
            button.addEventListener('click', function (event) {
                event.preventDefault();
                openHistoryPopup();
            });
        });
    }

    if (activeButton.length > 0) {
        activeButton.forEach(button => {
            button.addEventListener('click', function (event) {
                event.preventDefault();
                openActivePopup();
            });
        });
    }

    deliveryPopup.addEventListener('click', function (event) {
        if (event.target === deliveryPopup) {
            closeDeliveryPopup();
        }
    });

    historyPopup.addEventListener('click', function (event) {
        if (event.target === historyPopup) {
            closeHistoryPopup();
        }
    });

    activePopup.addEventListener('click', function (event) {
        if (event.target === activePopup) {
            closeActivePopup();
        }
    });
});