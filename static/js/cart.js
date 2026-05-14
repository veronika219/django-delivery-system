document.addEventListener('DOMContentLoaded', () => {

    console.log('cart.js loaded');

    document.addEventListener('click', function (e) {

        // =========================
        // ADD (menu)
        // =========================
        const addBtn = e.target.closest('.add-btn');
        if (addBtn) {
            increase(addBtn.dataset.id);
            return;
        }

        // =========================
        // PLUS
        // =========================
        const plusBtn = e.target.closest('.plus-btn');
        if (plusBtn) {
            increase(plusBtn.dataset.id);
            return;
        }

        // =========================
        // MINUS
        // =========================
        const minusBtn = e.target.closest('.minus-btn');
        if (minusBtn) {
            decrease(minusBtn.dataset.id);
            return;
        }

        // =========================
        // REMOVE (cart page)
        // =========================
        const removeBtn = e.target.closest('.remove-btn');
        if (removeBtn) {
            removeItem(removeBtn.dataset.id);
            return;
        }

    });

});


// =====================================
// INCREASE
// =====================================
function increase(id) {

    fetch(`/cart/ajax/increase/${id}/`)
        .then(res => res.json())
        .then(data => {

            syncControls(id, data.quantity);
            updateItemTotal(id, data.item_total);
            updateCartTotal(data.cart_total_price);
            updateHeader(data.cart_total_items);
        })
        .catch(err => console.log('INCREASE ERROR', err));
}


// =====================================
// DECREASE
// =====================================
function decrease(id) {

    fetch(`/cart/ajax/decrease/${id}/`)
        .then(res => res.json())
        .then(data => {

            if (data.empty_cart) {
                updateHeader(0);
                window.location.href = data.redirect_url;
                return;
            }

            if (data.removed) {
                removeProduct(id);
            } else {
                syncControls(id, data.quantity);
                updateItemTotal(id, data.item_total);
            }

            updateCartTotal(data.cart_total_price);
            updateHeader(data.cart_total_items);
        })
        .catch(err => console.log('DECREASE ERROR', err));
}


// =====================================
// REMOVE ITEM
// =====================================
function removeItem(id) {

    fetch(`/cart/ajax/remove/${id}/`)
        .then(res => res.json())
        .then(data => {

            if (data.empty_cart) {
                updateHeader(0);
                window.location.href = data.redirect_url;
                return;
            }

            removeProduct(id);
            updateCartTotal(data.cart_total_price);
            updateHeader(data.cart_total_items);
        })
        .catch(err => console.log('REMOVE ERROR', err));
}


// =====================================
// SYNC CONTROLS (menu + cart)
// =====================================
function syncControls(id, quantity) {

    document.querySelectorAll(`.cart-controls-${id}`).forEach(box => {

        let minusIcon = '−';

        if (quantity === 1) {
            minusIcon = '🗑️';
        }

        box.innerHTML = `
            <div class="d-flex gap-2 align-items-center">

                <button class="minus-btn btn btn-outline-dark btn-sm"
                        data-id="${id}">
                    ${minusIcon}
                </button>

                <span class="quantity-${id} fw-bold">
                    ${quantity}
                </span>

                <button class="plus-btn btn btn-dark btn-sm"
                        data-id="${id}">
                    +
                </button>

            </div>
        `;
    });
}


// =====================================
// REMOVE PRODUCT FROM UI
// =====================================
function removeProduct(id) {

    // MENU → show "Add"
    document.querySelectorAll(`.cart-controls-${id}`).forEach(box => {

        box.innerHTML = `
            <button class="add-btn btn btn-dark btn-sm"
                    data-id="${id}">
                Додати
            </button>
        `;
    });

    // CART → remove row
    document.querySelectorAll(`.cart-row-${id}`).forEach(row => {

        row.style.transition = '0.2s';
        row.style.opacity = '0';

        setTimeout(() => row.remove(), 200);
    });
}


// =====================================
// UPDATE ITEM TOTAL
// =====================================
function updateItemTotal(id, total) {

    document.querySelectorAll(`.item-total-${id}`).forEach(el => {
        el.innerText = total;
    });
}


// =====================================
// UPDATE CART TOTAL PRICE
// =====================================
function updateCartTotal(total) {

    const el = document.querySelector('#cart-total-price');

    if (el) {
        el.innerText = total;
    }
}


// =====================================
// UPDATE HEADER BADGE
// =====================================
function updateHeader(totalItems) {

    const badge = document.querySelector('#cart_total');

    if (!badge) return;

    totalItems = Number(totalItems || 0);

    if (totalItems <= 0) {
        badge.innerText = '';
        badge.style.display = 'none';
        return;
    }

    badge.style.display = 'inline-block';
    badge.innerText = totalItems;
}

