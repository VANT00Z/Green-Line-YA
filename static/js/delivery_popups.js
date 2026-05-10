document.addEventListener('DOMContentLoaded', function () {
    const deliveryButton = document.querySelectorAll('#open-order-popup');
    const historyButton = document.querySelectorAll('#open-history-popup');
    const activeButton = document.querySelectorAll('#open-active-popup');
    const closeButtons = document.querySelectorAll('.close-popup');

    const deliveryPopup = document.getElementById('delivery-popup');
    const historyPopup = document.getElementById('history-popup');
    const activePopup = document.getElementById('active-popup');

    const orderForm = document.getElementById('order-form');

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
        notification.style.animation = 'fadeIn 0.3s ease-in';

        document.body.appendChild(notification);

        setTimeout(() => {
            notification.remove();
        }, 3000);
    }

    async function handleOrderCreate(event) {
        event.preventDefault();

        const form = event.target;
        const address = form.querySelector('[name="delivery-address"]').value;
        const datetime = form.querySelector('[name="delivery-date"]').value;
        const weight = form.querySelector('[name="delivery-weight"]').value;
        const description = form.querySelector('[name="delivery-description"]').value;

        if (!address || !datetime || !weight) {
            showNotification('Заполните обязательные поля', true);
            return;
        }

        try {
            const response = await fetch('/create_order', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    address: address,
                    datetime: datetime,
                    weight: weight,
                    description: description
                })
            });

            const data = await response.json();

            if (data.success) {
                showNotification(data.message);
                form.reset();
                closeAll();
                setTimeout(() => {
                    location.reload();
                }, 1500);
            } else {
                showNotification(data.message, true);
            }
        } catch (error) {
            console.error('Ошибка:', error);
            showNotification('Ошибка сервера', true);
        }
    }

    async function loadActiveOrders() {
        const activeContent = document.getElementById('active-content');
        if (!activeContent) return;

        activeContent.innerHTML = '<div class="loading">Загрузка...</div>';

        try {
            const response = await fetch('/get_active_orders');
            const data = await response.json();

            if (data.success && data.orders.length > 0) {
                activeContent.innerHTML = data.orders.map(order => `
                    <div class="order-card">
                        <h4>Заказ #${order.id}</h4>
                        <p><strong>Адрес:</strong> ${order.address}</p>
                        <p><strong>Дата:</strong> ${order.date}</p>
                        <p><strong>Вес:</strong> ${order.weight} кг</p>
                        ${order.description ? `<p><strong>Описание:</strong> ${order.description}</p>` : ''}
                        <p class="order-date"><strong>Создан:</strong> ${order.created_at}</p>
                        <div class="order-actions">
                            <button onclick="cancelOrder(${order.id})" class="cancel-btn">Отменить заказ</button>
                        </div>
                    </div>
                `).join('');
            } else if (data.success) {
                activeContent.innerHTML = '<div class="empty-message">У вас нет активных заказов</div>';
            } else {
                activeContent.innerHTML = '<div class="empty-message">Ошибка загрузки заказов</div>';
            }
        } catch (error) {
            console.error('Ошибка:', error);
            activeContent.innerHTML = '<div class="empty-message">Ошибка загрузки заказов</div>';
        }
    }

    async function loadHistoryOrders() {
        const historyContent = document.getElementById('history-content');
        if (!historyContent) return;

        historyContent.innerHTML = '<div class="loading">Загрузка...</div>';

        try {
            const response = await fetch('/get_orders_history');
            const data = await response.json();

            if (data.success && data.orders.length > 0) {
                historyContent.innerHTML = data.orders.map(order => `
                    <div class="order-card">
                        <h4>Заказ #${order.id}</h4>
                        <p><strong>Адрес:</strong> ${order.address}</p>
                        <p><strong>Дата:</strong> ${order.date}</p>
                        <p><strong>Вес:</strong> ${order.weight} кг</p>
                        ${order.description ? `<p><strong>Описание:</strong> ${order.description}</p>` : ''}
                        <p class="order-date"><strong>Выполнен:</strong> ${order.created_at}</p>
                    </div>
                `).join('');
            } else if (data.success) {
                historyContent.innerHTML = '<div class="empty-message">История заказов пуста</div>';
            } else {
                historyContent.innerHTML = '<div class="empty-message">Ошибка загрузки истории</div>';
            }
        } catch (error) {
            console.error('Ошибка:', error);
            historyContent.innerHTML = '<div class="empty-message">Ошибка загрузки истории</div>';
        }
    }

    window.cancelOrder = async function (orderId) {
        if (confirm('Вы уверены, что хотите отменить этот заказ?')) {
            try {
                const response = await fetch(`/cancel_order/${orderId}`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    }
                });

                const data = await response.json();

                if (data.success) {
                    showNotification(data.message);
                    await loadActiveOrders();
                } else {
                    showNotification(data.message, true);
                }
            } catch (error) {
                console.error('Ошибка:', error);
                showNotification('Ошибка при отмене заказа', true);
            }
        }
    };

    function openDeliveryPopup() {
        deliveryPopup.style.display = 'block';
        closeHistoryPopup();
        closeActivePopup();
    }

    async function openHistoryPopup() {
        if (historyPopup) {
            await loadHistoryOrders();
            historyPopup.style.display = 'block';
        }
        closeDeliveryPopup();
        closeActivePopup();
    }

    async function openActivePopup() {
        if (activePopup) {
            await loadActiveOrders();
            activePopup.style.display = 'block';
        }
        closeDeliveryPopup();
        closeHistoryPopup();
    }

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

    closeButtons.forEach(button => {
        button.addEventListener('click', closeAll);
    });

    if (orderForm) {
        orderForm.addEventListener('submit', handleOrderCreate);
    }

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

const style = document.createElement('style');
style.textContent = `
    @keyframes fadeIn {
        from {
            opacity: 0;
            transform: translateX(20px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
`;
document.head.appendChild(style);