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

    if (!deliveryPopup || !historyPopup || !activePopup || !closeButton) {
        console.error('Один из элементов не найден в DOM');
        return;
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