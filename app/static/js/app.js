const tg = window.Telegram.WebApp;
tg.expand();

let cart = JSON.parse(localStorage.getItem('cart')) || [];

function addToCart(id, name, price) {
    let existing = cart.find(item => item.id === id);
    if (existing) {
        existing.quantity += 1;
    } else {
        cart.push({ id, name, price, quantity: 1 });
    }
    localStorage.setItem('cart', JSON.stringify(cart));
    updateMainButton();
}

function updateMainButton() {
    let totalCount = cart.reduce((sum, item) => sum + item.quantity, 0);
    if (totalCount > 0) {
        tg.MainButton.text = `View Order (${totalCount} items)`;
        tg.MainButton.show();
    } else {
        tg.MainButton.hide();
    }
}

tg.MainButton.onClick(() => {
    let user = tg.initDataUnsafe.user || {};
    
    fetch('/api/order', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            user_id: user.id || 123456,
            user_name: user.first_name || "Guest",
            cart: cart
        })
    })
    .then(res => res.json())
    .then(data => {
        if (data.success) {
            localStorage.removeItem('cart');
            window.location.href = `/success/${data.order_id}`;
        }
    });
});

updateMainButton();