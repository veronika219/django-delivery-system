
document.addEventListener('DOMContentLoaded', () => {

    console.log('cart.js loaded');

    document.addEventListener('click', async (e) => {

        // =========================
        // ADD
        // =========================

        if (e.target.classList.contains('add-btn')) {

            const id = e.target.dataset.id;

            increase(id);
        }

        // =========================
        // PLUS
        // =========================

        if (e.target.classList.contains('plus-btn')) {

            const id = e.target.dataset.id;

            increase(id);
        }

        // =========================
        // MINUS
        // =========================

        if (e.target.classList.contains('minus-btn')) {

            const id = e.target.dataset.id;

            decrease(id);
        }

        // =========================
        // REMOVE
        // =========================

        if (e.target.classList.contains('remove-btn')) {

            const id = e.target.dataset.id;

            removeItem(id);
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
        });
}


// =====================================
// DECREASE
// =====================================

function decrease(id) {

    fetch(`/cart/ajax/decrease/${id}/`)
        .then(res => res.json())
        .then(data => {

            // EMPTY CART
            if (data.empty_cart) {

                updateHeader(0);

                window.location.href = data.redirect_url;

                return;
            }

            // PRODUCT REMOVED
            if (data.removed) {

                removeProduct(id);

            } else {

                syncControls(id, data.quantity);

                updateItemTotal(id, data.item_total);
            }

            updateCartTotal(data.cart_total_price);

            updateHeader(data.cart_total_items);
        });
}


// =====================================
// REMOVE ITEM
// =====================================

function removeItem(id) {

    fetch(`/cart/ajax/remove/${id}/`)
        .then(res => res.json())
        .then(data => {

            // EMPTY
            if (data.empty_cart) {

                updateHeader(0);

                window.location.href = data.redirect_url;

                return;
            }

            removeProduct(id);

            updateCartTotal(data.cart_total_price);

            updateHeader(data.cart_total_items);
        });
}


// =====================================
// SYNC CONTROLS
// =====================================

function syncControls(id, quantity) {

    document
        .querySelectorAll(`.cart-controls-${id}`)
        .forEach(box => {

            let minus = '−';

            if (quantity === 1) {
                minus = '🗑️';
            }

            box.innerHTML = `
                <div class="d-flex gap-2 align-items-center">

                    <button
                        class="minus-btn btn btn-outline-dark btn-sm"
                        data-id="${id}"
                    >
                        ${minus}
                    </button>

                    <span class="quantity-${id} fw-bold">
                        ${quantity}
                    </span>

                    <button
                        class="plus-btn btn btn-dark btn-sm"
                        data-id="${id}"
                    >
                        +
                    </button>

                </div>
            `;
        });
}


// =====================================
// REMOVE PRODUCT
// =====================================

function removeProduct(id) {

    // MENU
    document
        .querySelectorAll(`.cart-controls-${id}`)
        .forEach(box => {

            box.innerHTML = `
                <button
                    class="add-btn btn btn-dark btn-sm"
                    data-id="${id}"
                >
                    Додати
                </button>
            `;
        });

    // CART ROW
    document
        .querySelectorAll(`.cart-row-${id}`)
        .forEach(row => {

            row.remove();
        });
}


// =====================================
// UPDATE ITEM TOTAL
// =====================================

function updateItemTotal(id, total) {

    document
        .querySelectorAll(`.item-total-${id}`)
        .forEach(el => {

            el.innerText = total;
        });
}


// =====================================
// UPDATE TOTAL PRICE
// =====================================

function updateCartTotal(total) {

    const el = document.querySelector('#cart-total-price');

    if (el) {

        el.innerText = total;
    }
}


// =====================================
// UPDATE HEADER
// =====================================

function updateHeader(totalItems) {

    const badge = document.querySelector('#cart_total');

    if (!badge) return;

    // HIDE
    if (totalItems <= 0) {

        badge.style.display = 'none';

        return;
    }

    // SHOW
    badge.style.display = 'inline-block';

    badge.innerText = totalItems;
}
