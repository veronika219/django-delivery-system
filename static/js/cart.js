document.addEventListener('DOMContentLoaded', () => {

    document.addEventListener('click',  (e) => {
        const addBtn = e.target.closest('.add-btn')
        if (addBtn) {

            const id = addBtn.dataset.id;

            increase(id);
        }

        const plusBtn = e.target.closest('.plus-btn')
        if (plusBtn) {

            const id = plusBtn.dataset.id;

            increase(id);
        }

        const minusBtn = e.target.closest('.minus-btn')
        if (minusBtn) {

            const id = minusBtn.dataset.id;

            decrease(id);
        }

        const removeBtn = e.target.closest('.remove-btn')
        if (removeBtn) {

            const id = removeBtn.dataset.id;

            removeItem(id);
        }

    });

});


function increase(id) {

    fetch(`/cart/ajax/increase/${id}/`)
        .then(res => res.json())
        .then(data => {

            if (!data.success) {
                return;
            }

            syncControls(id, data.quantity);

            updateItemTotal(id, data.item_total);

            updateCartTotal(data.cart_total_price);

            updateHeader(data.cart_total_items);
        });
}


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


// SYNC CONTROLS

function syncControls(id, quantity) {

    document
        .querySelectorAll(`.cart-controls-${id}`)
        .forEach(box => {

            let minus = '−';

            if (quantity === 1) {
                minus = '<i class="bi bi-trash"></i>';
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


// REMOVE PRODUCT

function removeProduct(id) {

    // MENU
    const box = document.querySelector(`.cart-controls-${id}`)
    if (box) {

        box.innerHTML = `
            <button
                class="add-btn btn-primary-custom"
                data-id="${id}"
            >
                Додати
            </button>
        `;
    }

    // CART ROW
    const row = document.querySelector(`.cart-row-${id}`)
    if (row) {

        row.remove()

    }
}


// UPDATE ITEM TOTAL

function updateItemTotal(id, total) {

    const el = document.querySelector(`.item-total-${id}`)

    if (el) {

        el.innerText = total;

    }
}


// UPDATE TOTAL PRICE
function updateCartTotal(total) {

    const el = document.querySelector('#cart-total-price');

    if (el) {

        el.innerText = total;
    }
}


// UPDATE HEADER
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
